###***********************************###
'''
Grade Notifier
File: grade_notifier.py
Author: Ehud Adler
Core Maintainers: Ehud Adler, Akiva Sherman,
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###

###********* Imports *********###
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
# Remote
from cunyfirstapi import Locations, CUNYFirstAPI
from bs4 import BeautifulSoup
from lxml import etree, html
from twilio.rest import Client
from os.path import join, dirname
from dotenv import load_dotenv
from login_flow.loginState import LoginState
from helper.userdata import User
from helper.message import Message
from helper.gpa import GPA
from helper.constants import instance_path, abs_repo_path
from helper import constants, fileManager, helper
from helper.helper import custom_hash
from helper.changelog import Changelog
from helper.refresh_result import RefreshResult
from helper.school_class import Class
from helper.redacted_stdout import RedactedPrint, STDOutOptions, RedactedFile

import requests
import getpass
import re
import argparse
import os
import atexit
import fileinput
import time
import logging
import traceback
import datetime
###********* GLOBALS *********###

# Create .env file path.
dotenv_path = join(constants.abs_repo_path(), '.env')

# Load file from the path.
load_dotenv(dotenv_path)

# Accessing variables.
account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

redacted_print_std = None
redacted_print_err = None
user = None
client = None
api = None
state = None
endtime = None

'''
    Sends a text message via Twilio

    Message: The body of the message
    Send Number: The number where the message should be sent
'''
def send_text(message, sendNumber):
    if state == LoginState.PROD:
        client.messages.create(
            from_=os.getenv('TWILIO_NUMBER'), to=sendNumber, body=message)
    else:
        print(
            "\n**********\nSENDING MESSAGE:\nFrom: 000-000-0000\nTo: {0}\nMessage: {1}\n"
            .format(sendNumber, message))


'''
    Converts a changelog array to a message
    Changelog: The list of classes which have had grade changes
'''
def create_text_message(change_log, is_welcome=False):

    # Message header
    new_message = None

    if is_welcome:
        new_message = welcome_message()
    else:
        new_message = Message()

    new_message \
        .add("New Grades have been posted for the following classes") \
        .newline() \
        .add("-------------") \
        .newline()

    class_num = 1
    gpa = change_log.gpa

    for elm in change_log.classes:
        if len(elm['grade']) != 0:
            new_message \
                .add("{0}. {1}".format(class_num, elm['name'])) \
                .newline()
            class_num += 1

    new_message \
        .newline() \
        .add("Grade for those classes are:") \
        .newline() \
        .add("----------------------------") \
        .newline()

    for elm in change_log.classes:
        if len(elm['grade']) != 0:
            new_message \
                .add("{0}: {1} (Grade) -- {2} (Grade Points)".format(
                    elm['name'], elm['grade'], elm['gradepts'])) \
                .newline()

    if gpa.get_term_gpa() >= 0:

        new_message.add("----------------------------") .newline() .add(
            "Your term GPA is: {0}".format(
                gpa.get_term_gpa())) .newline() .add(
            "Your cumulative GPA is: {0}".format(
                gpa.get_cumulative_gpa())) .newline()

        # Sign the message
        new_message.sign()

    return new_message.message()

'''
    Finds differences between 2 arrays of classes and returns the differences

    Old: Old Classes
    New: New Classes
'''
def find_changes(old, new):

    new_gpa = new.gpa
    changelog = []

    for i in range(0, len(new.classes)):
        class2 = new.classes[i]
        if i >= len(old.classes):
            changelog.append({
                'name': class2.name,
                'grade': class2.grade,
                'gradepts': class2.gradepts
            })
        else:
            class1 = old.classes[i]
            if class1.name == class2.name and class1 != class2:
                changelog.append({
                    'name': class2.name,
                    'grade': class2.grade,
                    'gradepts': class2.gradepts
                })

    return None if len(changelog) == 0 else Changelog(
        changelog, new_gpa)  # always add gpa to the list

###********* Main Program *********###

def welcome_message():
    new_message = Message()

    new_message \
        .add("👋 Welcome to the Grade Notifier 🚨") \
        .newline() \
        .newline() \
        .add("Your UID is: {0}".format(custom_hash(user.get_username()))) \
        .newline() \
        .add("You're all set up. You should see your current grades below!") \
        .newline() \
        .add("The notifier will message you whenever a grade changes (or is added)!") \
        .newline()
    return new_message

def sign_in(remaining_attempts=5):
    api.restart_session()
    api.login()
    if api.is_logged_in():
        return True
    elif remaining_attempts > 0:
        return sign_in(remaining_attempts-1)
    else:
        return False

def create_instance():
    sign_in(2)
    if api.is_logged_in():
        start_notifier(True)

def parse_grades_to_class(raw_grades):
    results = []
    for grade in raw_grades:
        new_class = Class(
            grade["name"],
            grade["description"],
            grade["units"],
            grade["grading"],
            grade["grade"],
            grade["gradepts"],
        )
        results.append(new_class)
    return results

def refresh(remaining_attempts=2):

    # If this is a re-attempt, sleep for 30 min between attempts
    if remaining_attempts != 2:
        time.sleep(30 * 60)

    # If no attempts remain, print error and end
    if remaining_attempts <= 0:
        print("Error refreshing. No attempts left.")
        exit(1)

    if not api.is_logged_in():
        if(sign_in()):
            refresh(remaining_attempts - 1)
        else:
            print("Error refreshing. Multiple logins failed")
            
    actObj = api.move_to(Locations.student_grades)

    # action.grades returns a dict of
    # results: [grades], term_gpa: term_gpa (float), 
    # cumulative_gpa: cumulative_gpa (float)
    raw_grades = actObj.grades()

    # Check if raw_grades is none, 
    # if so, retry
    if not raw_grades:
        refresh(remaining_attempts - 1)

    # do some perliminary checks on raw_grades to 
    # make sure the format is proper before
    # trying to access info
    if 'results' in raw_grades \
        and 'term_gpa' in raw_grades  \
        and 'cumulative_gpa' in raw_grades:
        try:
            raw_results = raw_grades['results']
            result = parse_grades_to_class(raw_results)
            return RefreshResult(
            result, 
            GPA(
                raw_grades['term_gpa'], 
                raw_grades['cumulative_gpa']
            )
        )  
        except ValueError:
            refresh(remaining_attempts - 1)
    else:
        # Check if any attempts remain
        # if non do, end the program with a 
        # final print statement expalaing the problem
        if not remaining_attempts:
            print("Error refreshing. No attempts left.")
        else:
            refresh(remaining_attempts - 1)

def start_notifier(is_welcome=False):
    old_result = RefreshResult([], -1)
    while datetime.datetime.now() < endtime:
        try:
            result = refresh()
        except TypeError:
            traceback.print_exc()
            print('[DEBUG] (TypeError, start_notifier) Trying again...')
            # Note this will not affect counter
            continue
        except ValueError:
            print('[DEBUG] (ValueError, start_notifier) Trying again...')
            # send message asking for more info to help us?
            pass
        changelog = find_changes(old_result, result) \
            if result != None \
            else None
        if changelog is not None:
            message = create_text_message(changelog, is_welcome)
            send_text(message, user.get_number())
            old_result = result
            is_welcome = False
        time.sleep(30 * 60)  # 30 min intervals


def check_user_exists(username):
    stored_username = custom_hash(username)
    file_path = instance_path(state)
    open(file_path, 'a').close()
    with open(file_path, 'r+') as file:
        return re.search(
            '^{0}'.format(re.escape(stored_username)), file.read(), flags=re.M)

def add_new_user_instance(username):
    file_path = instance_path(state)
    if not check_user_exists(username):    
        stored_username = custom_hash(username)
        with open(file_path, "a+") as instance_file:
            redacted_list = [username]
            instance_file = RedactedFile(instance_file, redacted_list)
            instance_file.write("{0} : {1}\n".format(stored_username,
                                                     os.getpid()))
        return True
    return False

def remove_user_instance(username):
    file_path = instance_path(state)
    file = ""

    if not os.path.isfile(file_path):
        return

    stored_username = custom_hash(username)
    with open(file_path) as oldfile:
        for line in oldfile:
            if stored_username not in line:
                file += line
    with open(file_path, 'w+') as newfile:
        redacted_list = [username]
        newfile = RedactedFile(newfile, redacted_list)
        newfile.writelines(file)

def exit_handler():
    send_text(constants.SESSION_ENDED_TEXT, user.get_number())
    remove_user_instance(user.get_username())

def already_in_session_message():
    return constants.ALREADY_IN_SESSION

def parse():
    parser = argparse.ArgumentParser(
        description='Specify commands for CUNY Grade Notifier Retriever v1.0')
    parser.add_argument('--school', default="QNS01")
    parser.add_argument('--list-codes', action='store_true')
    parser.add_argument('--username')
    parser.add_argument('--password')
    parser.add_argument('--phone')
    parser.add_argument('--filename')

    # Production
    parser.add_argument('--prod')

    # Development
    parser.add_argument('--enable_phone')

    return parser.parse_args()


def initialize_twilio():
    global client
    client = Client(account_sid, auth_token)


def main():
    global user
    global state
    global api
    global redacted_print_std
    global redacted_print_err
    global endtime

    args = parse()
    state = LoginState.determine_state(args)

    try:

        print(args)
        # Only initialize twilio in production
        # or when specifically asked
        if state == LoginState.PROD or args.enable_phone:
            initialize_twilio()
        
        username = input(
            "Enter username: ") if not args.username else args.username
        password = getpass.getpass(
            "Enter password: ") if not args.password else args.password
        number = input(
            "Enter phone number: ") if not args.phone else args.phone

        ## Monkey Patching stdout to remove any sens. data
        redacted_list = [username, password]
        redacted_print_std = RedactedPrint(STDOutOptions.STDOUT, redacted_list)
        redacted_print_err = RedactedPrint(STDOutOptions.ERROR, redacted_list)
        redacted_print_std.enable()
        redacted_print_err.enable()

        if add_new_user_instance(username):
            endtime = datetime.datetime.now() + datetime.timedelta(days=14)
            api = CUNYFirstAPI(username, password, args.school.upper())
            user = User(username, password, number, args.school.upper())
            atexit.register(exit_handler)
            create_instance()
        else:
            print(already_in_session_message())

    except Exception as e:
        print("ERROR")
        traceback.print_exc()
        # adding comment bc cant push


if __name__ == '__main__':
    main()

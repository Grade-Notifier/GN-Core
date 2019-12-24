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
from cunyfirstapi import Locations
from cunyfirstapi import CUNYFirstAPI
from bs4 import BeautifulSoup
from lxml import etree
from twilio.rest import Client
from lxml import html
from pprint import pprint
from cryptography.fernet import Fernet
from os.path import join, dirname
from dotenv import load_dotenv
from helper.userdata import User
from login_flow.loginState import LoginState
from helper.message import Message
from helper.gpa import GPA
from helper.constants import instance_path, abs_repo_path
from helper import constants
from helper import fileManager
from helper import helper
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
import mysql.connector
###********* GLOBALS *********###

# Create .env file path.
dotenv_path = join(constants.abs_repo_path(), '.env')

# Load file from the path.
load_dotenv()

# Accessing variables.
account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
DB_USERNAME = os.getenv('LOCALHOST_USERNAME')
DB_PASSWORD = os.getenv('LOCALHOST_PASSWORD')
key = os.getenv('DB_ENCRYPTION_KEY').encode('utf-8')

redacted_print_std = None
redacted_print_err = None
user = None
client = None
state = None

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
    new_message = Message()

    if is_welcome:
        new_message = welcome_message()

    new_message \
        .add("New Grades have been posted for the following classes") \
        .newline() \
        .add("-------------") \
        .newline()

    class_num = 1
    gpa = change_log.gpa

    for elm in change_log.classes:
        if len(elm.grade) != 0:
            new_message \
                .add("{0}. {1}".format(class_num, elm.name)) \
                .newline()
            class_num += 1

    new_message \
        .newline() \
        .add("Grade for those classes are:") \
        .newline() \
        .add("----------------------------") \
        .newline()

    for elm in change_log.classes:
        if len(elm.grade) != 0:
            new_message \
                .add("{0}: {1} (Grade) -- {2} (Grade Points)".format(
                    elm.name, elm.grade, elm.gradepts)) \
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


###********* Main Program *********###

def welcome_message():
    new_message = Message()

    new_message \
        .add("👋 Welcome to the Grade Notifier 🚨") \
        .newline() \
        .newline() \
        .add("You're all set up. You should see your current grades below!") \
        .newline() \
        .add("The notifier will message you whenever a grade changes (or is added)!") \
        .newline()
    return new_message



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

def refresh(api):
    actObj = api.move_to(Locations.student_grades)
    # action.grades returns a dict of
    # results: [grades], term_gpa: term_gpa (float), 
    # cumulative_gpa: cumulative_gpa (float)
    raw_grades = actObj.grades()

    if 'results' in raw_grades \
    and 'term_gpa' in raw_grades  \
    and 'cumulative_gpa' in raw_grades:
        result = parse_grades_to_class(raw_grades['results'])
        return RefreshResult(
            result, 
            GPA(
                raw_grades['term_gpa'], 
                raw_grades['cumulative_gpa']
            )
        )  
    else:
        # Couldn't get the proper grade from 
        # cunyfirstapi just try and refresh
        return refresh(api)

def start_notifier():

    myconnector = mysql.connector.Connect(user=DB_USERNAME,
        host='localhost',passwd=DB_PASSWORD)

    cursor = myconnector.cursor()
    myconnector.autocommit = True
    cursor.execute('USE GradeNotifier')
    while True:
        global key
        cursor.execute('''SELECT * FROM Users WHERE lastUpdated < NOW() - INTERVAL 30 MINUTE ORDER BY lastUpdated DESC LIMIT 1''') # get top row from 
        # cursor.execute('''SELECT * FROM Users LIMIT 1''')
        try: 
            row = cursor.next()
            column_names = cursor.column_names

            query_dict = {k: v for k,v in zip(column_names, row)}
            pprint(query_dict)

            if query_dict['lastUpdated'].year == 1970:
                is_welcome = True
            else:
                is_welcome = False

            cursor.execute(f'UPDATE Users SET lastUpdated = NOW() WHERE id={query_dict["id"]};')

            encrypted_password = query_dict['password']

            

            f = Fernet(key)
            password = f.decrypt(encrypted_password.encode('utf-8')).decode()

            api = CUNYFirstAPI(query_dict['username'], password, query_dict['school'].upper())
            api.login()

            grade_result= refresh(api)

            frozen_set_grades = frozenset(grade_result.classes)
            grade_hash = str(hash(frozen_set_grades))

            '''
            IMPORTANT NOTE!!!
            Hash seed value changes each time you run so you need 
            to set the hash seed to be the same each time
            so when running this script, run it as
            PYTHONHASHSEED=0 python3 ...
            '''

            print(grade_hash)
            if grade_hash != query_dict['gradeHash']:
                # we have a difference
                print('GRADE DIFFERENCE, SENDING MESSAGE!')
                message = create_text_message(grade_result, is_welcome)
                send_text(message, query_dict['phoneNumber'])

                cursor.execute(f'UPDATE Users SET gradeHash = {grade_hash} WHERE id={query_dict["id"]};')

            
            api.logout()

            

        except StopIteration:
            pass
        except:
            traceback.print_exc()
        time.sleep(1)
       



def exit_handler():
    send_text(constants.SESSION_ENDED_TEXT, user.get_number())
    remove_user_instance(user.get_username())


def already_in_session_message():
    return constants.ALREADY_IN_SESSION


def parse():
    parser = argparse.ArgumentParser(
        description='Specify commands for CUNY Grade Notifier Retriever v1.0')

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

    args = parse()
    state = LoginState.determine_state(args)

    try:
        # Only initialize twilio in production
        # or when specifically asked
        if state == LoginState.PROD or args.enable_phone:
            initialize_twilio()
        
        start_notifier()

    except: 
        traceback.print_exc()


if __name__ == '__main__':
    main()

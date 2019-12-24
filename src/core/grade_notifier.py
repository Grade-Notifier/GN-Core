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
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from cunyfirstapi import Locations
from cunyfirstapi import CUNYFirstAPI
from bs4 import BeautifulSoup
from lxml import etree
from twilio.rest import Client
from lxml import html
from os.path import join, dirname
from dotenv import load_dotenv
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
import datetime
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
auth_token  = os.getenv('TWILIO_AUTH_TOKEN')

# Database 
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST     = os.getenv('DB_HOST')

# Encryption
PRIVATE_RSA_KEY = os.getenv('PRIVATE_RSA_KEY').replace(r'\n', '\n')

myconnector = None
redacted_print_std = None
redacted_print_err = None
client = None
state  = None

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


def create_connection():
    global myconnector
    try:
        myconnector = mysql.connector.Connect(
            user=DB_USERNAME,
            host=DB_HOST,
            passwd=DB_PASSWORD
        )
    except Error as e:
        print("Error while connecting to MySQL", e)

def get_cursor():
    if myconnector.is_connected():
        cursor = myconnector.cursor()
        myconnector.autocommit = True
        cursor.execute('USE GradeNotifier')
        return cursor
    return None

def start_notifier():

    create_connection()
    cursor = get_cursor()

    if cursor == None:
        return

    while True:
        global WAIT_INTERVAL

        cursor.execute('''SELECT * FROM Users \
                                   WHERE lastUpdated < NOW() - INTERVAL 30 MINUTE \
                                   ORDER BY lastUpdated DESC LIMIT 1'''
        ) # get top row from 
        for row in cursor:
            try: 
                column_names = cursor.column_names

                query_dict = {k: v for k,v in zip(column_names, row)}

                phoneNumber         = query_dict['phoneNumber']
                last_updated        = query_dict['lastUpdated']
                username            = query_dict['username']
                school              = query_dict['school']
                grade_hash          = query_dict['gradeHash']
                encrypted_password  = query_dict['password']
                date_created        = query_dict['dateCreated']
                __id                = query_dict['id']

                is_welcome = last_updated.year == 1970

                cursor.execute(f'UPDATE Users SET lastUpdated = NOW() WHERE id={__id};')
                
                private_key_object = RSA.importKey(PRIVATE_RSA_KEY)
                cipher = PKCS1_OAEP.new(private_key_object)

                byte_string = bytes.fromhex(encrypted_password)

                decrypted_password = cipher.decrypt(byte_string).decode()

                api = CUNYFirstAPI(username, decrypted_password, school.upper())
                api.login()

                grade_result = refresh(api)
                grade_hash = str(hash(frozenset(grade_result.classes)))

                if grade_hash != query_dict['gradeHash']:
                    message = create_text_message(grade_result, is_welcome)
                    send_text(message, phoneNumber)
                    cursor.execute(f'UPDATE Users SET gradeHash = {grade_hash} WHERE id={__id};')

                api.logout()
                remove_user_if_necessary(cursor, username, date_created)
            except StopIteration:
                pass

            except:
                traceback.print_exc()
        time.sleep(constants.WAIT_INTERVAL)

'''
Check to see if the use has not received any new grades in {DAYS_TILL_REMOVED} days. If so, remove them.
'''
def remove_user_if_necessary(cursor, username, date_created):
    if datetime.datetime.now() > date_created + datetime.timedelta(days=constants.DAYS_TILL_REMOVED):
        query = 'DELETE FROM Users WHERE username=%s'
        data = (username,)
        try:
            cursor.execute(query, data)
        except mysql.connector.IntegrityError as err:
            print(err)
            traceback.print_exc()

def parse():
    parser = argparse.ArgumentParser(
        description='Specify commands for CUNY Grade Notifier Retriever v1.0')
   
    parser.add_argument('--prod')         # Production
    parser.add_argument('--enable_phone') # Development
    return parser.parse_args()

def initialize_twilio():
    global client
    client = Client(account_sid, auth_token)

def main():
    global state

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

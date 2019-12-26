###***********************************###
'''
Grade Notifier
File: initializegn.py
Author: Ehud Adler
Core Maintainers: Ehud Adler, Akiva Sherman,
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###

from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import mysql.connector
import argparse
import time
import os
import re
import requests
import getpass
import traceback
import subprocess
import cunyfirstapi
from helper import constants
from lxml import html
from helper.fileManager import create_dir
from helper.constants import log_path
from helper.constants import script_path, abs_repo_path
from helper.helper import print_to_screen
from helper.security import decrypt
from dotenv import load_dotenv
from os.path import join, dirname

"""Initialize Grade-Notifier
"""

__author__ = "Ehud Adler & Akiva Sherman"
__copyright__ = "Copyright 2018, The Punk Kids"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Ehud Adler & Akiva Sherman"
__email__ = "self@ehudadler.com"
__status__ = "Production"

# Load file.
load_dotenv()

# Accessing variables.
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
PRIVATE_RSA_KEY = os.getenv('PRIVATE_RSA_KEY').replace(r'\n', '\n')

def add_to_db(username, encrypted_password, school, phone):

    myconnector = mysql.connector.Connect(user=DB_USERNAME,
            host=DB_HOST, passwd=DB_PASSWORD)
    cursor = myconnector.cursor()
    myconnector.autocommit = True
    cursor.execute('USE GradeNotifier')

    query_string = (f'''INSERT INTO Users (username, password, school, phoneNumber) VALUES '''
            f'''(%s, %s, %s, %s);''')

    # query_string = myconnector.converter.escape(query_string)
    # print(query_string)
    data = (username, encrypted_password, school, phone)
    cursor.execute(query_string, data)



def user_exists(username, school):
    myconnector = mysql.connector.Connect(user=DB_USERNAME,
            host=DB_HOST, passwd=DB_PASSWORD)
    cursor = myconnector.cursor()
    myconnector.autocommit = True
    cursor.execute('USE GradeNotifier')

    # test if in DB by checking count of records with that username and school combo
    query_string = ('''SELECT COUNT(*) FROM Users WHERE '''
            f'''username = %s AND school = %s''')

    data = (username, school)
    cursor.execute(query_string, data)
    rows = cursor.next()[0]
    return rows > 0

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


def main():
    args = parse()
    try:
        username = input(
            "Enter username: ") if not args.username else args.username
        encrypted_password = getpass.getpass(
            "Enter password: ") if not args.password else args.password
        number = input(
            "Enter phone number: ") if not args.phone else args.phone
        prod = False if not args.prod else True


        username = re.sub(r'@login\.cuny\.edu', '', username).lower()
        if user_exists(username, args.school.upper()):
            print_to_screen(
                "Seems that you already have a session running.\n" \
                + "If you think there is a mistake, contact me @ Ehud.Adler62@qmail.cuny.edu",
                "error",
                "Oh No!",
            )
            return

        password = decrypt(encrypted_password, 'keys/private.pem')
        
        api = cunyfirstapi.CUNYFirstAPI(username, password)
        api.login()
        if api.is_logged_in():
            add_to_db(username, encrypted_password, args.school.upper(), number)
            print_to_screen(
                "Check your phone for a text!\n" \
                + "The service will check for new grades every 30 min and text you when anything changes.\n" \
                + "The service will continue for 2 weeks and then require you to sign-in again.\n" \
                + "Please only sign in once.\n" \
                + "Enjoy!",
                "ok",
                "Hold Tight!",
            )

            api.logout()
        else:
            print_to_screen(
                "The username/password combination you entered seems to be invalid.\n" \
                + "Please try again.",
                "error",
                "Oh No!",
            )


    except Exception as e:
        traceback.print_exc()


if __name__ == '__main__':
    main()

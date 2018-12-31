"""Grade-Notifier               
"""

__author__      = "Ehud Adler & Akiva Sherman"
__copyright__   = "Copyright 2018, The Punk Kids"
__license__     = "MIT"
__version__     = "1.0.0"
__maintainer__  = "Ehud Adler & Akiva Sherman"
__email__       = "self@ehudadler.com"
__status__      = "Production"

###********* Imports *********###

## Local
import constants
import helper

from helper import State
from helper import Message
from helper import Session
from cunylogin import login

from constants import instance_path
from constants import script_path

import constants
import helper

## Remote
import requests
import getpass
import re
import argparse
import os
import atexit
import fileinput

from bs4 import BeautifulSoup
from lxml import etree
from twilio.rest import Client
from lxml import html
from os.path import join, dirname
from dotenv import load_dotenv

###********* GLOBALS *********###

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')

# Load file from the path.
load_dotenv(dotenv_path)

# Accessing variables.
account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

session = None
client = None
state = None

###********* Helper Methods *********###

'''
    Holds details for a class to be compared later

    Name: Short class name
    Description: Long class name 
    Units: Number of credits its worth
    Grading: Undergraduate vs Graduate
    Grade: Letter Grade
    Grade Points: Units * Letter grade value
'''
class Class():
    def __init__(self, name, description, units, grading, grade, gradepts):
        self.name = name
        self.description = description
        self.units = units
        self.grading = grading
        self.grade = grade
        self.gradepts = gradepts

    def __eq__(self, other):
        return self.grade == other.grade \
                and self.gradepts == other.gradepts

'''
    Sends a text message via Twilio

    Message: The body of the message
    Send Number: The number where the message should be sent
'''
def send_text(message, sendNumber):
    if state == State.PROD:
        client.messages.create(
            from_= os.getenv('TWILIO_NUMBER'),
            to=sendNumber,
            body=message
        )
    else:
        print("\n**********\nSENDING MESSAGE:\nFrom: 000-000-0000\nTo: {0}\nMessage: {1}\n".format(sendNumber, message))

'''
    Converts a changelog array to a message

    Changelog: The list of classes which have had grade changes
'''
def create_text_message(change_log):

    # Message header
    new_message = Message()

    new_message \
    .add("New Grades have been posted for the following classes") \
    .newline() \
    .add("-------------") \
    .newline()

    class_num = 1
    for elm in change_log:
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

    for elm in change_log:
        if len(elm['grade']) != 0:
            new_message \
            .add("{0}: {1} (Grade) -- {2} (Grade Points)".format(
                elm['name'], elm['grade'], elm['gradepts'])) \
            .newline()

    # Sign the message
    new_message.sign()

    return new_message.message()

'''
    Finds differences between 2 arrays of classes and returns the differences

    Old: Old Classes
    New: New Classes
'''
def find_changes(old, new):

    changelog = []
    for i in range(0, len(new)):
        class2 = new[i]
        if i >= len(old):
            changelog.append(
                {'name': class2.name, 'grade': class2.grade, 'gradepts': class2.gradepts})
        else:
            class1 = old[i]
            if class1.name == class2.name and class1 != class2:
                changelog.append(
                    {'name': class2.name, 'grade': class2.grade, 'gradepts': class2.gradepts})

    return None if len(changelog) == 0 else changelog


###********* Main Program *********###

def create_instance(session, username, password, number, school_code):
    login(session, username, password)
    if session.is_logged_in():
        start_notifier(session, number, school_code, username, password)
    else:
        ## Login failed
        pass

def refresh(session, school):

    session.current.get(constants.CUNY_FIRST_GRADES_URL)

    payload = {'ICACTION': 'DERIVED_SSS_SCT_SSS_TERM_LINK'}
    try:
    	response = session.current.post(constants.CUNY_FIRST_GRADES_URL, data=payload)
    except TimeoutError:
    	return refresh(session,school)

    tree = html.fromstring(response.text)

    payload_key = ''.join(tree.xpath('//span[text()="2018 Fall Term"]/parent::div/parent::td/preceding-sibling::td/div/input/@id'))
    payload_value = ''.join(tree.xpath('//span[text()="2018 Fall Term"]/parent::div/parent::td/preceding-sibling::td/div/input/@value'))

    payload = {
        payload_key: payload_value,
        'ICACTION': 'DERIVED_SSS_SCT_SSR_PB_GO'
    }
    try:
    	response = session.current.post(constants.CUNY_FIRST_GRADES_URL, data=payload)
    except TimeoutError:
    	return refresh(session,school)


    	
    tree = BeautifulSoup(response.text, 'lxml')
    good_html = tree.prettify()
    soup = BeautifulSoup(good_html, 'html.parser')
    table = soup.find('table', attrs={'class': "PSLEVEL1GRIDWBO"})

    result = []
    if table is not None:
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            row_marker += 1
            columns = row.find_all('td')
            data = []
            for column in columns:
                if row_marker > 1:
                    data.append(column.get_text())
                column_marker += 1
            if len(data) is not 0:
                new_class = Class(data[0].strip(), data[1].strip(), data[2].strip(
                ), data[3].strip(), data[4].strip(), data[5].strip())
                result.append(new_class)
    else:
        pass
    return result


def start_notifier(session, number, school, username, password):
    counter = 0
    old_result = []
    while counter < 844:
        if session.is_logged_in():
            result = refresh(session, school)
            if len(old_result) > len(result):
                pass
            else:
                changelog = find_changes(old_result, result)
                if changelog != None:
                    message = create_text_message(changelog)
                    send_text(message, number)
                    old_result = result
                time.sleep(5*60)  # 5 Min intervals
                counter += 1
        else:
            login(session, username, password)


def check_user_exists(username):
    file_path = instance_path(state)
    with open(file_path, 'r+') as file:
        return re.search('^{0}'.format(re.escape(username)), file.read(), flags=re.M)

def add_new_user_instance(username):
    file_path = instance_path(state)
    if not check_user_exists(username.lower()):
        with open(file_path, "a+") as instance_file:
            instance_file.write("{0} : {1}\n".format(username.lower(), os.getpid()))
        return True
    return False

def remove_user_instance(username):
    file_path = instance_path(state)
    file = ""

    if not os.path.isfile(file_path):
        return

    with open(file_path) as oldfile:
        for line in oldfile:
            if not username.lower() in line:
                file += line
    with open(file_path, 'w+') as newfile:
            newfile.writelines(file)


def exit_handler():
    send_text(constants.SESSION_ENDED_TEXT, session.get_number())
    remove_user_instance(session.get_username())

def already_in_session_message():
    return constants.ALREADY_IN_SESSION

###********* Tests *********###

def test_add_remove():
    username = "FOO-BAR"
    add_new_user_instance(username)
    user_exists = check_user_exists(username.lower())
    remove_user_instance(username)
    user_removed = check_user_exists(username.lower())
    return user_exists and not user_removed

def test_message_contructions():
    l1 = [{'name': "0", 'grade': "5", 'gradepts': "5"}, {'name': "3", 'grade': "4", 'gradepts': "5"}]
    message = create_text_message(l1)
    return message == '''

    '''

def test_diff():
    l1 = [Class("0","1","2","3","4","5"), Class("2","1","2","3","4","5")]
    l2 = [Class("0","1","2","4","5","5"), Class("2","1","2","3","4","5"), Class("3","1","2","3","4","5")]
    l3 = find_changes(l1, l2)
    return l3 == [{'name': "0", 'grade': "5", 'gradepts': "5"}, {'name': "3", 'grade': "4", 'gradepts': "5"}]

def parse():
    parser = argparse.ArgumentParser(description='Specify commands for CUNY Grade Notifier Retriever v1.0')
    parser.add_argument('--school', default="QNS01")
    parser.add_argument('--list-codes', action='store_true')
    parser.add_argument('--username')
    parser.add_argument('--password')
    parser.add_argument('--phone')
    parser.add_argument('--filename')

    ## Production
    parser.add_argument('--prod') 

    ## Development
    parser.add_argument('--enable_phone')

    ## Testing 
    parser.add_argument('--test')
    parser.add_argument('--test_diff')
    parser.add_argument('--test_add_remove_instance')
    parser.add_argument('--test_message_contruction')
    return parser.parse_args()


def run_test(args):

    passed_test = True

    if args.test_diff:
        passed_test = test_diff()
    elif args.test_add_remove_instance:
        passed_test = test_add_remove()
    elif args.test_message_contruction:
        passed_test = test_message_contructions()
    else:
        print("This test does not exists")
    
    if passed_test:
        print("Test Passed")
    else:
        print("Test Failed")

def initialize_twilio():
    client = Client(account_sid, auth_token)

def main():
    global session
    args = parse()
    state = State.determine_state(args)
    try:
        if state == State.TEST:
            run_test(args)
        else:

            # Only initialize twilio in production 
            # or when specifically asked
            if state == State.PROD or args.enable_phone:
                initialize_twilio()

            s = requests.Session()
            s.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
            username = input("Enter username: ") if not args.username else args.username
            password = getpass.getpass("Enter password: ") if not args.password else args.password
            number = input("Enter phone number: ") if not args.phone else args.phone

            if add_new_user_instance(username):
                session = Session(s, username, password, number)
                atexit.register(exit_handler)
                create_instance(session, username, password,
                                number, args.school.upper())
            else:
                print(already_in_session_message())

    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()

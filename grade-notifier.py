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

client = Client(account_sid, auth_token)

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
    client.messages.create(
        from_= os.getenv('TWILIO_NUMBER'),
        to=sendNumber,
        body=message
    )

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

    message \
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
    start_notifier(session, number, school_code, username, password)

def login(session, username, password):
    print('[**] Logging in...')

    session.get(CUNY_FIRST_HOME_URL)

    ## AUTH LOGIN

    data = {
        'usernameH': f'{username}@login.cuny.edu',
        'username': username,
        'password': password,
        'submit': ''
    }
    session.post(CUNY_FIRST_AUTH_SUBMIT_URL, data=data)

    ## STUDENT CENTER
    response = session.get(CUNY_FIRST_STUDENT_CENTER_URL)
    tree = html.fromstring(response.text)
    encquery = tree.xpath('//*[@name="enc_post_data"]/@value')[0]

    data = {
        'enc_post_data': encquery
    }
    response = session.post(CUNY_FIRST_LOGIN-URL, data=data)

    tree = html.fromstring(response.text)
    encreply = tree.xpath('//*[@name="enc_post_data"]/@value')[0]

    data = {
        'enc_post_data': encreply
    }
    session.post(CUNY_FIRST_LOGIN_2_URL, data=data)

    response = session.get(CUNY_FIRST_SIGNED_IN_STUDENT_CENTER_URL)
    print('[**] Successfully logged in!')
    return response


def refresh(session, school):

    session.get(CUNY_FIRST_GRADES_URL)

    payload = {'ICACTION': 'DERIVED_SSS_SCT_SSS_TERM_LINK'}
    response = session.post(CUNY_FIRST_GRADES_URL, data=payload)

    tree = html.fromstring(response.text)

    payload_key = ''.join(tree.xpath('//span[text()="2018 Fall Term"]/parent::div/parent::td/preceding-sibling::td/div/input/@id'))
    payload_value = ''.join(tree.xpath('//span[text()="2018 Fall Term"]/parent::div/parent::td/preceding-sibling::td/div/input/@value'))

    payload = {
        payload_key: payload_value,
        'ICACTION': 'DERIVED_SSS_SCT_SSR_PB_GO'
    }
    response = session.post(CUNY_FIRST_GRADES_URL, data=payload)

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
        print("Trouble parsing")
    return result


def start_notifier(session, number, school, username, password):
    counter = 0
    old_result = []
    while counter < 844:
        result = refresh(session, school)
        if len(old_result) > len(result):
            login(session, username, password)
        else:
            changelog = find_changes(old_result, result)
            if changelog != None:
                message = create_text_message(changelog)
                send_text(message, number)
                old_result = result
            time.sleep(5*60)  # 5 Min intervals
            counter += 1


def check_user_exists(user, is_test):
    file_path = instance_path(is_test)
    with open(file_path, 'r') as file:
        return re.search('^{0}$'.format(re.escape(user)), file.read(), flags=re.M)

def add_new_user_instance(username, is_test):
    file_path = instance_path(is_test)
    if not check_user_exists(username.lower(), file_path):
        with open(file_path, "a") as instance_file:
            instance_file.write("{0}\n".format(username.lower()))
        return True
    return False

def remove_user_instance(username, is_test):
    file_path = instance_path(is_test)
    file = ""
    with open(file_path) as oldfile:
        for line in oldfile:
            if not username.lower() in line:
                file += line
    with open(file_path, 'w') as newfile:
            newfile.writelines(file)


def exit_handler():
    send_text(SESSION_ENDED_TEXT, number)
    remove_user_instance(username, False)

def already_in_session_message():
    return ALREADY_IN_SESSION

###********* Tests *********###

def test_add_remove():
    username = "FOO-BAR"
    add_new_user_instance(username, True)
    user_exists = check_user_exists(username.lower(), True)
    remove_user_instance(username, True)
    user_removed = check_user_exists(username.lower(), True)
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



def main():
    try:
        parser = argparse.ArgumentParser(description='Specify commands for CUNY Grade Notifier Retriever v1.0')
        parser.add_argument('--school', default="QNS01")
        parser.add_argument('--list-codes', action='store_true')
        parser.add_argument('--username')
        parser.add_argument('--password')
        parser.add_argument('--phone')
        parser.add_argument('--filename')

        ## Testing 
        parser.add_argument('--test')
        parser.add_argument('--test_diff')
        parser.add_argument('--test_add_remove_instance')
        parser.add_argument('--test_message_contruction')

        args = parser.parse_args()

        if args.test:

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

        else:

            session = requests.Session()
            session.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
            username = input("Enter username: ") if not args.username else args.username
            password = getpass.getpass("Enter password: ") if not args.password else args.password
            number = input("Enter phone number: ") if not args.phone else args.phone

            if add_new_user_instance(username, None):
                atexit.register(exit_handler)
                create_instance(session, username, password,
                                number, args.school.upper())
            else:
                print(already_in_session_message())

    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()

# Grade Notifier
# Ehud Adler
# Akiva Sherman
# 12.23.18

# Enjoy!


###********* Imports *********###

import requests
import getpass
import re
import datetime
import time
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

# College names and codes pulled from the CunyFirst website
college_codes = {
    'BAR01': 'Baruch College',
    'BMC01': 'Borough of Manhattan CC',
    'BCC01': 'Bronx CC',
    'BKL01': 'Brooklyn College',
    'CTY01': 'City College',
    'CSI01': 'College of Staten Island',
    'GRD01': 'Graduate Center',
    'NCC01': 'Guttman CC',
    'HOS01': 'Hostos CC',
    'HTR01': 'Hunter College',
    'JJC01': 'John Jay College',
    'KCC01': 'Kingsborough CC',
    'LAG01': 'LaGuardia CC',
    'LEH01': 'Lehman College',
    'MHC01': 'Macaulay Honors College',
    'MEC01': 'Medgar Evers College',
    'NYT01': 'NYC College of Technology',
    'QNS01': 'Queens College',
    'QCC01': 'Queensborough CC',
    'SOJ01': 'School of Journalism',
    'SLU01': 'School of Labor&Urban Studies',
    'LAW01': 'School of Law',
    'MED01': 'School of Medicine',
    'SPS01': 'School of Professional Studies',
    'SPH01': 'School of Public Health',
    'UAPC1': 'University Processing Center',
    'YRK01': 'York College'
}

# Load file from the path.
load_dotenv(dotenv_path)

# Accessing variables.
account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)

instance_file_url = "/home/fa18/313/adeh6562/public_html/grade-notifier/instances.txt"
test_instance_file_url = "/home/fa18/313/adeh6562/public_html/grade-notifier/test-instances.txt"

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
        if self.grade == other.grade \
                and self.gradepts == other.gradepts:
            return True
        else:
            return False

'''
    Sends a text message via Twilio

    Message: The body of the message
    Send Number: The number where the message should be sent
'''
def send_text(message, sendNumber):
    client.messages.create(
        from_='+12013806942',
        to=sendNumber,
        body=message
    )

'''
    Converts a changelog array to a message

    Changelog: The list of classes which have had grade changes
'''
def create_text_message(change_log):

    # Message header
    message = "Grade Alert 🚨 from Grade Notifier\n\n"
    message += "New Grades have been posted for the following classes\n-------------\n"

    class_num = 1
    for elm in change_log:
        if len(elm['grade']) != 0:
            message += "{0}. {1}\n".format(class_num, elm['name'])
            class_num += 1

    message += "\nGrade for those classes are:\n-------------\n"

    for elm in change_log:
        if len(elm['grade']) != 0:
            message += "{0}: {1} (Grade) -- {2} (Grade Points) \n".format(
                elm['name'], elm['grade'], elm['gradepts'])

    return sign_message(message)


def sign_message(message):
    message += "\nHope you did well! -- Ehud & Akiva"
    return message


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

    if len(changelog) == 0:
        return None
    return changelog


###********* Main Program *********###

def create_instance(session, username, password, number, school_code):
    login(session, username, password)
    start_notifier(session, number, school_code, username, password)

def login(session, username, password):
    print('[**] Logging in...')
    session.get('https://home.cunyfirst.cuny.edu')

    url = 'https://ssologin.cuny.edu/oam/server/auth_cred_submit'
    data = {
        'usernameH': f'{username}@login.cuny.edu',
        'username': username,
        'password': password,
        'submit': ''
    }

    r = session.post(url, data=data)

    url = 'https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?FolderPath=PORTAL_ROOT_OBJECT.HC_SSS_STUDENT_CENTER&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder&PortalActualURL=https%3a%2f%2fhrsa.cunyfirst.cuny.edu%2fpsc%2fcnyhcprd%2fEMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL&PortalContentURL=https%3a%2f%2fhrsa.cunyfirst.cuny.edu%2fpsc%2fcnyhcprd%2fEMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL&PortalContentProvider=HRMS&PortalCRefLabel=Student%20Center&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2fhome.cunyfirst.cuny.edu%2fpsp%2fcnyepprd%2f&PortalURI=https%3a%2f%2fhome.cunyfirst.cuny.edu%2fpsc%2fcnyepprd%2f&PortalHostNode=EMPL&NoCrumbs=yes&PortalKeyStruct=yes'
    r = session.get(url)
    tree = html.fromstring(r.text)

    encquery = tree.xpath('//*[@name="enc_post_data"]/@value')[0]

    url = 'https://ssologin.cuny.edu/obrareq.cgi'
    data = {
        'enc_post_data': encquery
    }

    r = session.post(url, data=data)

    tree = html.fromstring(r.text)
    encreply = tree.xpath('//*[@name="enc_post_data"]/@value')[0]

    url = 'https://hrsa.cunyfirst.cuny.edu/obrar.cgi'
    data = {
        'enc_post_data': encreply
    }
    r = session.post(url, data=data)

    url = 'https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?FolderPath=PORTAL_ROOT_OBJECT.HC_SSS_STUDENT_CENTER&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder&PortalActualURL=https%3a%2f%2fhrsa.cunyfirst.cuny.edu%2fpsc%2fcnyhcprd%2fEMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL&PortalContentURL=https%3a%2f%2fhrsa.cunyfirst.cuny.edu%2fpsc%2fcnyhcprd%2fEMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL&PortalContentProvider=HRMS&PortalCRefLabel=Student%20Center&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2fhome.cunyfirst.cuny.edu%2fpsp%2fcnyepprd%2f&PortalURI=https%3a%2f%2fhome.cunyfirst.cuny.edu%2fpsc%2fcnyepprd%2f&PortalHostNode=EMPL&NoCrumbs=yes&PortalKeyStruct=yes'
    r = session.get(url)
    print('[**] Successfully logged in!')
    return r


def refresh(session, school):

    url = 'https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL?Page=SSR_SSENRL_GRADE&Action=A&TargetFrameName=None'

    session.get(url)

    payload = {'ICACTION': 'DERIVED_SSS_SCT_SSS_TERM_LINK'}
    r = session.post(url, data=payload)

    tree = html.fromstring(r.text)

    payload_key = ''.join(tree.xpath('//span[text()="2018 Fall Term"]/parent::div/parent::td/preceding-sibling::td/div/input/@id'))
    payload_value = ''.join(tree.xpath('//span[text()="2018 Fall Term"]/parent::div/parent::td/preceding-sibling::td/div/input/@value'))

    payload = {payload_key: payload_value,
               'ICACTION': 'DERIVED_SSS_SCT_SSR_PB_GO'}
    r = session.post(url, data=payload)

    tree = BeautifulSoup(r.text, 'lxml')
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


def check_user_exists(user, test_file):
    file_path = instance_file_url if not test_file else test_file
    with open(instance_file_url, 'r') as file:
        if re.search('^{0}$'.format(re.escape(user)), file.read(), flags=re.M):
            return True
        else:
            return False

def add_new_user_instance(username, test_file):
    file_path = instance_file_url if not test_file else test_file
    if not check_user_exists(username.lower(), None):
        with open(file_path, "a") as instance_file:
            instance_file.write("{0}\n".format(username.lower()))
        return True
    return False

def remove_user_instance(username, test_file):
    file_path = instance_file_url if not test_file else test_file
    with open(instance_file_url) as oldfile:
        for line in oldfile:
            if not username.lower() in line:
                file += line
    with open(instance_file_url, 'w') as newfile:
            newfile.writelines(file)


def exit_handler():
    remove_user_instance(username, None)

def already_in_session_message():
    return "This username already has an instance running. You should recieve a text message when a grade changes. Please contact me @ Ehud.Adler62@qmail.cuny.edu if you have any futher questions"

###********* Tests *********###

def test_add_remove():
    add_new_user_instance("FOO-BAR", test_instance_file_url)
    user_exists = check_user_exists("FOO-BAR", test_instance_file_url)
    remove_user_instance("FOO-BAR", test_instance_file_url)
    user_removed = check_user_exists("FOO-BAR", test_instance_file_url)
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

if __name__ == '__main__':
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

            if add_new_user_instance(username):
                atexit.register(exit_handler)
                create_instance(session, username, password,
                                number, args.school.upper())
            else:
                print(already_in_session_message())


    except Exception as e:
        print(str(e))

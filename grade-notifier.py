# Grade Notifier
# Ehud Adler
# Akiva Sherman
# 12.23.18

# Enjoy!

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

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')

# Load file from the path.
load_dotenv(dotenv_path)

# Accessing variables.
# account_sid = os.getenv('TWILIO_SID')
# auth_token = os.getenv('TWILIO_AUTH_TOKEN')

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

# # account_sid = os.environ["twilio_account_sid"]
# # auth_token = os.environ['twilio_auth_token']

account_sid = '***REMOVED***'
auth_token = '***REMOVED***'

client = Client(account_sid, auth_token)

instance_file_url = "./instances.txt"

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


def send_text(message, sendNumber):

    client.messages.create(
        from_='***REMOVED***',
        to=sendNumber,
        body=message
    )


def create_text_message(change_log):
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

    message += "\nHope you did well! -- Ehud & Akiva"
    return message


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


def create_instance(session, username, password, number, school_code):
    login(session, username, password)
    start_notifier(session, number, school_code)


def login(session, username, password):
    print('[DEBUG] Logging in...')
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
    print('[DEBUG] Successfully logged in!')
    password = None
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


def start_notifier(session, number, school):
    counter = 0
    old_result = []
    while counter < 844:
        result = refresh(session, school)
        if len(old_result) > len(result):
            send_text("Your session has timed out. You need to sign in again", number)
            break
        else:
            changelog = find_changes(old_result, result)
            if changelog != None:
                message = create_text_message(changelog)
                send_text(message, number)
                old_result = result
            time.sleep(5*60)  # 5 Min intervals
            counter += 1


def check_use_exists(user):
    with open(instance_file_url, 'r') as file:
        if re.search('^{0}$'.format(re.escape(user)), file.read(), flags=re.M):
            return True
        else:
            return False

def add_new_user_instance(username):
    if not check_use_exists(username.lower()):
        with open(instance_file_url, "a") as instance_file:
            instance_file.write("{0}\n".format(username.lower()))
        return True
    return False


def exit_handler():
    file = ""
    with open(instance_file_url) as oldfile:
        for line in oldfile:
            if not username.lower() in line:
                file += line
    with open(instance_file_url, 'w') as newfile:
            newfile.writelines(file)

def test_change():
    l1 = [Class("0","1","2","3","4","5"),Class("2","1","2","3","4","5")]
    l2 = [Class("0","1","2","4","5","5"),Class("2","1","2","3","4","5"), Class("3","1","2","3","4","5")]
    print(find_changes(l1, l2))



if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(
            description='Specify commands for CUNY Grade Notifier Retriever v1.0')
        parser.add_argument('--school', default="QNS01")
        parser.add_argument('--list-codes', action='store_true')
        parser.add_argument('--username')
        parser.add_argument('--password')
        parser.add_argument('--phone')
        parser.add_argument('--filename')
        args = parser.parse_args()

        session = requests.Session()
        session.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        username = input(
            "Enter username: ") if not args.username else args.username
        password = getpass.getpass(
            "Enter password: ") if not args.password else args.password
        number = input(
        "Enter phone number: ") if not args.phone else args.phone

        # test_change()

        if add_new_user_instance(username):
            atexit.register(exit_handler)
            create_instance(session, username, password,
                            number, args.school.upper())
        else:
            print("This username already has an instance running. You should recieve a text message when a grade changes. Please contact me @ Ehud.Adler62@qmail.cuny.edu if you have any futher questions")


    except Exception as e:
        print(str(e))

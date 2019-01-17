###***********************************###
'''
Grade Notifier
File: constants.py
Author: Ehud Adler
Core Maintainers: Ehud Adler, Akiva Sherman,
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###

from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import socket
from login_flow.loginState import LoginState

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

INSTANCE_ABS_PATH = "/home/fa18/313/adeh6562/public_html/grade-notifier/instances.txt"

INSTANCE_ABS_PATH_TEST = "/home/fa18/313/adeh6562/public_html/grade-notifier" \
    + "/test-instances.txt"

INSTANCE_ABS_PATH_DEV = "./instances.txt"

SCRIPT_PATH = "/home/fa18/313/adeh6562/public_html/grade-notifier/Grade-Notifier/src/core"
SCRIPT_PATH_DEV = "./src/core"

CUNY_FIRST_HOME_URL = "https://home.cunyfirst.cuny.edu"
CUNY_FIRST_AUTH_SUBMIT_URL = "https://ssologin.cuny.edu/oam/server/auth_cred_submit"

REPO_ABS_DIRECTORY_PATH = "/home/fa18/313/adeh6562/public_html/grade-notifier/Grade-Notifier"

CUNY_FIRST_STUDENT_CENTER_URL = "https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE" \
    + "/HRMS/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?FolderPath" \
    + "=PORTAL_ROOT_OBJECT.HC_SSS_STUDENT_CENTER&IsFolder" \
    + "=false&IgnoreParamTempl=FolderPath%2cIsFolder&PortalActualURL" \
    + "=https%3a%2f%2fhrsa.cunyfirst.cuny.edu%2fpsc%2fcnyhcprd%2f" \
    + "EMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL" \
    + "&PortalContentURL=https%3a%2f%2fhrsa.cunyfirst.cuny.edu%2fpsc" \
    + "%2fcnyhcprd%2fEMPLOYEE%2fHRMS%2fc%2f" \
    + "SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL&PortalContentProvider" \
    + "=HRMS&PortalCRefLabel=Student%20Center&PortalRegistryName" \
    + "=EMPLOYEE&PortalServletURI=https%3a%2f%2fhome.cunyfirst.cuny.edu" \
    + "%2fpsp%2fcnyepprd%2f&PortalURI" \
    + "=https%3a%2f%2fhome.cunyfirst.cuny.edu%2fpsc%2fcnyepprd%2f" \
    + "&PortalHostNode=EMPL&NoCrumbs=yes&PortalKeyStruct=yes"

CUNY_FIRST_LOGIN_URL = "https://ssologin.cuny.edu/obrareq.cgi"
CUNY_FIRST_LOGIN_2_URL = "https://hrsa.cunyfirst.cuny.edu/obrar.cgi"

CUNY_FIRST_SIGNED_IN_STUDENT_CENTER_URL = "https://hrsa.cunyfirst.cuny.edu/psc" \
    + "/cnyhcprd/EMPLOYEE/HRMS/c" \
    + "/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?FolderPath" \
    + "=PORTAL_ROOT_OBJECT.HC_SSS_STUDENT_CENTER&IsFolder" \
    + "=false&IgnoreParamTempl=FolderPath%2cIsFolder&PortalActualURL" \
    + "=https%3a%2f%2fhrsa.cunyfirst.cuny.edu%2fpsc%2fcnyhcprd" \
    + "%2fEMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL&" \
    + "PortalContentURL=https%3a%2f%2fhrsa.cunyfirst.cuny.edu" \
    + "%2fpsc%2fcnyhcprd%2fEMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES." \
    + "SSS_STUDENT_CENTER.GBL&PortalContentProvider=HRMS&PortalCRefLabel" \
    + "=Student%20Center&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2f" \
    + "home.cunyfirst.cuny.edu%2fpsp%2fcnyepprd%2f&PortalURI" \
    + "=https%3a%2f%2fhome.cunyfirst.cuny.edu%2fpsc%2fcnyepprd%2f&PortalHostNode" \
    + "=EMPL&NoCrumbs=yes&PortalKeyStruct=yes"

CUNY_FIRST_GRADES_URL = "https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS/c/" \
    + "SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL?Page=SSR_SSENRL_GRADE&Action" \
    + "=A&TargetFrameName=None"

ALREADY_IN_SESSION = "This username already has an instance running. " \
    + "You should recieve a text message when a grade changes. " \
    + "Please contact me @ Ehud.Adler62@qmail.cuny.edu if you have any futher questions"

SESSION_ENDED_TEXT = "Your session has ended. " \
    + "If you'd like to continue using Grade-Notifier please sign back in at "\
    + "https://venus.cs.qc.cuny.edu/~adeh6562/index.php"

CUNY_FIRST_HOME_URL_TEST = 'https://home.cunyfirst.cuny.edu/psp/cnyepprd/EMPLOYEE/EMPL/h/?tab=DEFAULT'
CUNY_FIRST_LOGOUT_URL = 'https://home.cunyfirst.cuny.edu/psp/cnyepprd/EMPLOYEE/EMPL/?cmd=logout'
CUNY_FIRST_LOGOUT_2_URL = 'https://home.cunyfirst.cuny.edu/sso/logout?end_url=https://home.cunyfirst.cuny.edu'
CUNY_FIRST_LOGOUT_3_URL = 'https://ssologin.cuny.edu/oamsso-bin/logout.pl?end_url=https%3A' \
    + '%2F%2Fhome.cunyfirst.cuny.edu'

LOG_PATH = "/home/fa18/313/adeh6562/public_html/grade-notifier/logs"
LOG_PATH_DEV = "./logs"



def abs_repo_path():
    return REPO_ABS_DIRECTORY_PATH

def is_local():
    return not ((socket.gethostname() == 'mars' or socket.gethostname() == 'venus'))

def log_path():
    if is_local():
        return LOG_PATH_DEV
    else:
        return LOG_PATH

def script_path():
    if is_local():
        return SCRIPT_PATH_DEV
    else:
        return SCRIPT_PATH

def instance_path(state=LoginState.DEV):
    if state == LoginState.PROD:
        return INSTANCE_ABS_PATH
    elif state == LoginState.TEST:
        return INSTANCE_ABS_PATH_TEST
    else:
        return INSTANCE_ABS_PATH_DEV

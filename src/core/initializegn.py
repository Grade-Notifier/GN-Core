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

import argparse
import time
import os
import requests
import getpass
import subprocess
import cunyfirstapi
from helper import constants
from lxml import html
from helper.fileManager import create_dir
from helper.session import Session
from helper.constants import log_path
from helper.constants import script_path, abs_repo_path
from helper.helper import print_to_screen
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

# Create .env file path.
dotenv_path = join(constants.abs_repo_path(), '.env')

# Load file from the path.
load_dotenv(dotenv_path)

# Accessing variables.
account_pass = os.getenv('ACCOUNT_PASSWORD')

def run(username, password, school, phone):
    log_path = '{0}/{1}{2}'.format(
        constants.log_path(), username, time.time())
    create_dir(constants.log_path())
    if constants.is_local():
        with open("{0}.txt".format(log_path), "w+") as outfile:
            subprocess.Popen(["nohup",
                              "python3",
                              f"{constants.script_path()}/grade_notifier.py",
                              f"--username={username}",
                              f"--password={password}",
                              f"--school={school}",
                              f"--phone={phone}"],
                             stdout=outfile)
    else:
        with open("{0}.txt".format(log_path), "w+") as outfile:
            subprocess.Popen(
                [
                    "nohup",
                    "setsid",
                    "python3",
                    f"{constants.script_path()}/grade_notifier.py",
                    f"--username={username}",
                    f"--password={password}",
                    f"--school={school}",
                    f"--phone={phone}",
                    "--prod=true"],
                stdout=outfile)


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
        password = getpass.getpass(
            "Enter password: ") if not args.password else args.password
        number = input(
            "Enter phone number: ") if not args.phone else args.phone
        prod = False if not args.prod else True

        api = cunyfirstapi.CUNYFirstAPI(username, password)
        if api.is_logged_in():
            run(username, password, args.school.upper(), number)
            print_to_screen(
                "Check your phone for a text!\n" \
                + "The service will check for new grades every 5 min and text you when anything changes.\n" \
                + "The service will continue for 5 days and then require you to sign-in again.\n" \
                + "Please only sign in once.\n" \
                + "Enjoy!"
            )
        else:
            print_to_screen(
                "The username/password combination you entered seems to be invalid.\n" \
                + "Please try again."
            )

    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()

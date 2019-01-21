###***********************************###
'''
Grade Notifier
File: terminategn.py
Author: Ehud Adler
Core Maintainers: Ehud Adler, Akiva Sherman,
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###

from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from login_flow.loginState import LoginState

import re
import argparse
import os
from helper.constants import instance_path, abs_repo_path
from helper.helper import cutsome_hash
from helper import constants
import subprocess


state = None

def parse():
    parser = argparse.ArgumentParser(
        description='Specify username to kill')
    parser.add_argument('--username')
    parser.add_argument('--prod')

    return parser.parse_args()


def getpid(username):
    stored_username = cutsome_hash(username)
    file_path = instance_path(state)

    if not os.path.isfile(file_path):
        return

    with open(file_path) as oldfile:
        for line in oldfile:
            if stored_username in line:
                return line.split(':')[1].strip()


def kill(username):
    stored_username = cutsome_hash(username)
    pid = getpid(stored_username)
    if pid:
    	subprocess.run(['kill','-SIGINT',pid])



def main():
    global state
    args = parse()
    state = LoginState.determine_state(args)
    username = args.username if args.username else input("Enter username: ")
    kill(username)
    



if __name__ == '__main__':
    main()
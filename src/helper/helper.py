###***********************************###
'''
Grade Notifier
File: helper.py
Author: Ehud Adler
Core Maintainers: Ehud Adler, Akiva Sherman,
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###

import hashlib

def print_to_screen(text, status=False, title=False):
    '''Prepend "RENDER::" to any text that must be printed on the website.
    If it is a status indicator, prepend "RENDER::STATUS::".
    If it is a page title, prepend "RENDER::TITLE::".'''
    if not (status or title):
        print("RENDER::" + text)
    elif status:
        print('RENDER::STATUS::' + text)
    elif title:
        print('RENDER::TITLE::' + text)
    else:
        print('BAD print_to_screen() PARAMETERS. ATTEMPTED TO PRINT: ' + text)


def custom_hash(username):
    peppered_username = username.lower() + 'asdf'
    peppered_username = peppered_username.encode('utf-8')
    hashed_username = hashlib.sha256(peppered_username).hexdigest()
    return hashed_username
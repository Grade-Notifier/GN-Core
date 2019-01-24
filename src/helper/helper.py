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


'''
    Style: RENDER:: --status="ok" --title="Hold tight" 
    --message="This is my message"
'''
def print_to_screen(text, status=None, title=None):
    pstr = "RENDER:: "

    if status:
        pstr += f'--status="{status}" '
    if title:
        pstr += f'--title="{title}" '

    pstr += f'--title="{text}"'
    print(pstr)

def custom_hash(username):
    peppered_username = username.lower() + 'asdf'
    peppered_username = peppered_username.encode('utf-8')
    hashed_username = hashlib.sha256(peppered_username).hexdigest()
    return hashed_username
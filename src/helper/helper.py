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

def print_to_screen(text):
    print("RENDER::" + text)

def custom_hash(username):
	peppered_username = username.lower() + 'asdf'
	hashed_username = hashlib.sha256(peppered_username).hexdigest()
	return hashed_username
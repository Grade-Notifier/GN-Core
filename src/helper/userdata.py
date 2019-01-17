###***********************************###
'''
Grade Notifier
File: userdata.py
Author: Ehud Adler
Core Maintainers: Ehud Adler, Akiva Sherman,
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###

class User():
    def __init__(self, username, password, number, school_code = None):
        self._username = username
        self._password = password
        self._number = number
        self._school_code = school_code

    def set_username(self, username):
        self._username = username

    def set_password(self, password):
        self._password = password

    def set_number(self, number):
        self._number = number

    def set_school_code(self, school_code):
        self._school_code = school_code

    def get_school_code(self):
        return self._school_code

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password

    def get_number(self):
        return self._number
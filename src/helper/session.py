from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import helper.constants
"""Session
"""

__author__ = "Ehud Adler & Akiva Sherman"
__copyright__ = "Copyright 2018, The Punk Kids"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Ehud Adler & Akiva Sherman"
__email__ = "self@ehudadler.com"
__status__ = "Production"


class SessionState():
    SIGNED_IN = 0
    SIGNED_OUT = 1


class Session():
    state = None
    current = None
    username = None
    password = None
    number = None

    def __init__(self, new_session, new_username, new_password, new_number):
        self.current = new_session
        self.username = new_username
        self.password = new_password
        self.number = new_number

    def set_username(self, new_username):
        self.username = new_username

    def set_password(self, new_password):
        self.password = new_password

    def set_number(self, new_number):
        self.number = new_number

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_number(self):
        return self.number

    def refresh_state(self):
        r = self.current.get(
            constants.CUNY_FIRST_HOME_URL_TEST,
            allow_redirects=False)
        self.state = SessionState.SIGNED_OUT if r.status_code == 302 else SessionState.SIGNED_IN

    def is_logged_in(self):
        self.refresh_state()
        return self.state == SessionState.SIGNED_IN

    def set_state(self, new_state):
        self.state = new_state

"""Helper
Holds the helper methods
"""

__author__      = "Ehud Adler & Akiva Sherman"
__copyright__   = "Copyright 2018, The Punk Kids"
__license__     = "MIT"
__version__     = "1.0.0"
__maintainer__  = "Ehud Adler & Akiva Sherman"
__email__       = "self@ehudadler.com"
__status__      = "Production"




class State():
    TEST = 0
    DEV  = 1
    PROD = 2

    @staticmethod
    def determine_state(args):
        if args.test:
            return State.TEST
        else if args.dev:
            return State.DEV
        else:
            return State.PROD

class Message():
    _message = "Grade Alert 🚨 from Grade Notifier\n\n"

    def message():
        return _message

    def newline():
        _message += "\n"
        return self

    def add(text):
        _message += text
        return self
    
    def sign():
         _message += "\nHope you did well! -- Ehud & Akiva"
         return self
###***********************************###
'''
Grade Notifier
File: loginState.py
Author: Ehud Adler
Core Maintainers: Ehud Adler, Akiva Sherman,
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###

class LoginState():
    TEST = 0
    DEV = 1
    PROD = 2

    @staticmethod
    def determine_state(args):
        if args.prod:
            return LoginState.PROD
        else:
            # The default is development
            print("Running in dev mode.....")
            return LoginState.DEV

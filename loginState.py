"""Login State
"""

__author__      = "Ehud Adler & Akiva Sherman"
__copyright__   = "Copyright 2018, The Punk Kids"
__license__     = "MIT"
__version__     = "1.0.0"
__maintainer__  = "Ehud Adler & Akiva Sherman"
__email__       = "self@ehudadler.com"
__status__      = "Production"

class LoginState():
    TEST = 0
    DEV  = 1
    PROD = 2

    @staticmethod
    def determine_state(args):
        if args.test:
            print("Running in test mode.....")
            return LoginState.TEST
        elif args.prod:
            return LoginState.PROD
        else:
            # The default is development
            print("Running in dev mode.....")
            return LoginState.DEV
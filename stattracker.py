"""Stat Tracker
"""

__author__      = "Ehud Adler & Akiva Sherman"
__copyright__   = "Copyright 2018, The Punk Kids"
__license__     = "MIT"
__version__     = "1.0.0"
__maintainer__  = "Ehud Adler & Akiva Sherman"
__email__       = "self@ehudadler.com"
__status__      = "Production"

import Crypto.hasher

class StatTracker():

     @staticmethod
     def add_grade_stat(usr, subject, teacher, grade):
        usr = Crypto.hasher.sha256(usr)
        #TODO get teacher, add to db

     

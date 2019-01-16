###***********************************###
'''
Grade Notifier
File: changelog.py
Author: Ehud Adler
Core Maintainers: Ehud Adler, Akiva Sherman, 
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###

class Changelog():
    def __init__(self, classes, gpa):
        self.classes = classes
        self.gpa = gpa

    def __eq__(self, other):
        return self.classes == other.classes \
            and self.gpa == other.gpa
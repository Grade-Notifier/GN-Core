"""Changelog
"""

__author__ = "Ehud Adler & Akiva Sherman"
__copyright__ = "Copyright 2018, The Punk Kids"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Ehud Adler & Akiva Sherman"
__email__ = "self@ehudadler.com"
__status__ = "Production"

class Changelog():
    def __init__(self, classes, gpa):
        self.classes = classes
        self.gpa = gpa

    def __eq__(self, other):
        return self.classes == other.classes \
            and self.gpa == other.gpa
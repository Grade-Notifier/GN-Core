"""GPA Class
"""

__author__      = "Ehud Adler & Akiva Sherman"
__copyright__   = "Copyright 2018, The Punk Kids"
__license__     = "MIT"
__version__     = "1.0.0"
__maintainer__  = "Ehud Adler & Akiva Sherman"
__email__       = "self@ehudadler.com"
__status__      = "Production"


class GPA():
    _term_gpa = 0
    _cumulative_gpa = 0

    def __init__(self,term_gpa = 0, cumulative_gpa = 0):
        self._term_gpa = term_gpa
        self._cumulative_gpa = cumulative_gpa

    def get_cumulative_gpa(self):
        return self._cumulative_gpa

    def get_term_gpa(self):
        return self._term_gpa

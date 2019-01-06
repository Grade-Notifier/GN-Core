"""GPA Class
"""

__author__ = "Ehud Adler & Akiva Sherman"
__copyright__ = "Copyright 2018, The Punk Kids"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Ehud Adler & Akiva Sherman"
__email__ = "self@ehudadler.com"
__status__ = "Production"


class GPA():
    _term_gpa = 0

    _cumulative_gpa = 0

    def __init__(self, term_gpa=0, cumulative_gpa=0):
        self._term_gpa = term_gpa
        self._cumulative_gpa = cumulative_gpa

    def get_cumulative_gpa(self):
        return self._cumulative_gpa

    def get_term_gpa(self):
        return self._term_gpa

    @staticmethod
    def get_letter_grade(gpa):
        return {
            'term_gpa': GPA.convert_float(gpa.get_term_gpa()),
            'cumulative_gpa': GPA.convert_float(gpa.get_cumulative_gpa())
        }

    @staticmethod
    def get_number_grade(gpa):
        return {
            'term_gpa':
            GPA.convert_letter(GPA.convert_float(gpa.get_term_gpa())),
            'cumulative_gpa':
            GPA.convert_letter(GPA.convert_float(gpa.get_cumulative_gpa()))
        }

    @staticmethod
    def convert_float(f):
        if 0 <= f < 1:
            return 'F'
        elif 1 <= f < 1.3:
            return 'D'
        elif 1.3 <= f < 1.7:
            return 'D+'
        elif 1.7 <= f < 2:
            return 'C-'
        elif 2 <= f < 2.3:
            return 'C'
        elif 2.3 <= f < 2.7:
            return 'C+'
        elif 2.7 <= f < 3:
            return 'B-'
        elif 3 <= f < 3.3:
            return 'B'
        elif 3.3 <= f < 3.7:
            return 'B+'
        elif 3.7 <= f < 4:
            return 'A-'
        else:
            return 'A'

    @staticmethod
    def convert_letter(l):
        scale = {
            'A+': '97 - 100',
            'A': '93 - 96',
            'A-': '90 - 92',
            'B+': '87 - 89',
            'B': '83 - 86',
            'B-': '80 - 82',
            'C+': '77 - 79',
            'C': '73 - 76',
            'C-': '70 - 72',
            'D+': '67 - 69',
            'D': '65 - 66',
            'F': '0'
        }
        return scale[l]

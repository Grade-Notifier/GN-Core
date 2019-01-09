"""Class
"""

__author__ = "Ehud Adler & Akiva Sherman"
__copyright__ = "Copyright 2018, The Punk Kids"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Ehud Adler & Akiva Sherman"
__email__ = "self@ehudadler.com"
__status__ = "Production"

###********* Helper Methods *********###
'''
    Holds details for a class to be compared later

    Name: Short class name
    Description: Long class name
    Units: Number of credits its worth
    Grading: Undergraduate vs Graduate
    Grade: Letter Grade
    Grade Points: Units * Letter grade value
'''
class Class():
    def __init__(self, name, description, units, grading, grade, gradepts):
        self.name = name
        self.description = description
        self.units = units
        self.grading = grading
        self.grade = grade
        self.gradepts = gradepts

    def __eq__(self, other):
        return self.grade == other.grade \
            and self.gradepts == other.gradepts
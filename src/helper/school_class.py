###***********************************###
'''
Grade Notifier
File: school_class.py
Author: Ehud Adler
Core Maintainers: Ehud Adler, Akiva Sherman,
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###

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
###***********************************###
'''
Grade Notifier
File: fileManager.py
Author: Ehud Adler
Core Maintainers: Ehud Adler, Akiva Sherman, 
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###

from os import sys, path
import os
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from helper import constants

def create_dir(dir_path):
    try:
        os.makedirs(dir_path)
        print("Directory ", dir_path, " Created ")
    except FileExistsError:
        pass

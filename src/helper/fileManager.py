import helper.constants
"""File Manager
helps with file managment
"""

__author__ = "Ehud Adler & Akiva Sherman"
__copyright__ = "Copyright 2018, The Punk Kids"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Ehud Adler & Akiva Sherman"
__email__ = "self@ehudadler.com"
__status__ = "Production"

from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


def create_dir(dir_path):
    try:
        os.makedirs(dir_path)
        print("Directory ", dir_path, " Created ")
    except FileExistsError:
        pass

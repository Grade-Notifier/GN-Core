from constants import instance_path
from constants import script_path
import argparse
import os
"""Test-Grade-Notifier
"""

__author__ = "Ehud Adler & Akiva Sherman"
__copyright__ = "Copyright 2018, The Punk Kids"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Ehud Adler & Akiva Sherman"
__email__ = "self@ehudadler.com"
__status__ = "Production"


def parse():
    parser = argparse.ArgumentParser(
        description='Specify commands for CUNY Grade Notifier Retriever v1.0')

    # Development
    parser.add_argument('--local')
    return parser.parse_args()


def run_test(args):

    scriptpath = script_path(args.local)
    instancepath = instance_path(args.local)

    print("Starting test suite.....")

    print("1. Pylint")
    os.system('pylint grade-notifier.py')

    print("\n2. Testing Diff")
    os.system(
        'python3 {0}grade-notifier.py --test=true --test_diff=true'
        .format(scriptpath)
    )

    print("\n3. Testing Add/Remove Instance")

    if os.path.isfile(instancepath):
        os.system('rm {0}'.format(instancepath))

    os.system('touch {0}'.format(instancepath))
    os.system(
        'python3 {0}grade-notifier.py --test=true --test_add_remove_instance=true'
        .format(scriptpath)
    )
    os.system('rm {0}'.format(instancepath))

    print("\n4. Testing Message Construction")
    os.system(
        'python3 {0}grade-notifier.py --test=true --test_message_construction=true'
        .format(scriptpath)
    )

    print('\n5. Testing GPA Class')
    os.system(
        'python3 {0}grade-notifier.py --test=true --test_gpa_class=true'
        .format(scriptpath)
    )


def main():
    args = parse()
    run_test(args)


if __name__ == '__main__':
    main()

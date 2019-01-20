###***********************************###
'''
Grade Notifier
File: tests.py
Author: Ehud Adler
Core Maintainers: Ehud Adler, Akiva Sherman, 
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###

from os import sys, path
import io

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from helper.helper import print_to_screen
from helper.constants import script_path, instance_path
from helper.message import Message
from helper.gpa import GPA
from helper.redacted_stdout import RedactedPrint, \
    STDOutOptions, RedactedFile
from core.grade_notifier import Class, find_changes, \
    create_text_message, add_new_user_instance, \
    check_user_exists, remove_user_instance, \
    RefreshResult, Changelog
import unittest
import os
import argparse
import cunyfirstapi
from core.terminategn import getpid as terminate_get_pid

class TestMessageClass(unittest.TestCase):

    def test_construction(self):
        message = Message()

        self.assertEqual(
            message.message(),
            'Grade Alert 🚨 from Grade Notifier\n\n')

        message \
            .add("Foo") \
            .add("Bar") \
            .add("Baz")

        message.newline()

        message.add("foo")
        self.assertEqual(
            message.message(),
            'Grade Alert 🚨 from Grade Notifier\n\n' +
            'FooBarBaz\nfoo')

        message.sign()
        self.assertEqual(
            message.message(),
            'Grade Alert 🚨 from Grade Notifier\n\n' +
            'FooBarBaz\nfoo\nHope you did well! -- Ehud & Akiva')


class TestGPAClass(unittest.TestCase):

    def test_gpa_converter(self):
        correct_letter_answers = {
            0: 'F',
            1: 'D',
            1.5: 'D+',
            2: 'C',
            2.5: 'C+',
            3: 'B',
            3.5: 'B+',
            4: 'A'
        }
        for num in correct_letter_answers.keys():
            g = GPA(num, num)
            grades = GPA.get_letter_grade(g)
            self.assertFalse(grades['term_gpa'] != correct_letter_answers[num])
            self.assertFalse(grades['cumulative_gpa'] !=
                             correct_letter_answers[num])


class TestDiffMethod(unittest.TestCase):
    def test_diff(self):
        l1 = [
            Class("0", "1", "2", "3", "4", "5"),
            Class("2", "1", "2", "3", "4", "5")
        ]
        l2 = [
            Class("0", "1", "2", "4", "5", "5"),
            Class("2", "1", "2", "3", "4", "5"),
            Class("3", "1", "2", "3", "4", "5")
        ]

        rr1 = RefreshResult(l1, 3.1)
        rr2 = RefreshResult(l2, 3.3)

        cl1 = find_changes(rr1, rr2)

        l4 = [{
            'name': "0",
            'grade': "5",
            'gradepts': "5"
        }, {
            'name': "3",
            'grade': "4",
            'gradepts': "5"
        }]

        cl2 = Changelog(l4, 3.3)

        self.assertEqual(cl1, cl2)

class TestAddRemoveNewUserMethod(unittest.TestCase):
    def test_add_remove(self):
        username = "FOO-BAR1"
        add_new_user_instance(username)
        pids = [str(os.getpid())]            # import our own pid
        pids.append(terminate_get_pid(username))

        remove_user_instance(username)

        username = "FOO-BAR2"
        add_new_user_instance(username)
        #pids = [os.getpid()]            # import our own pid
        pids.append(terminate_get_pid(username))

        remove_user_instance(username)

        username = "FOO-BAR3"
        add_new_user_instance(username)
        #pids = [os.getpid()]            # import our own pid
        pids.append(terminate_get_pid(username))

        remove_user_instance(username)
        passed = all(pid == str(os.getpid()) for pid in pids)

        self.assertTrue(passed)

class TestRedactPrint(unittest.TestCase):
    def test_redact(self):
        username = "Foo"
        password = "Bar"
        redacted = "REDACTED"

        print_statment = f"{username}'s password is {password}," \
            + "don't tell anyone"

        redacted_print = f"{redacted}'s password is {redacted}," \
            + "don't tell anyone"

        outcome = None

        redacted_list = [username, password]
        redacted_print_std = RedactedPrint(
            STDOutOptions.STDOUT, 
            redacted_list
        )

        redacted_print_std.enable()

        file_path = "./TEST_REDACT.txt"
        with open(file_path, "w+") as content_file:
            content_file = RedactedFile(
                content_file, 
                redacted_list
            )
            content_file.write(print_statment)

        with open(file_path, 'r') as content_file:
            outcome = content_file.read()

        os.remove(file_path)
        self.assertEqual(redacted_print, outcome)

class TestPrintToScreenMethod(unittest.TestCase):
    def test_print_to_screen(self):
        old_stdout = sys.stdout # Memorize the default stdout stream
        sys.stdout = buffer = io.StringIO()
        string_to_print = "This text should be displayed!"
        print_to_screen(string_to_print)
        sys.stdout = old_stdout # Put the old stream back in place
        expected = "RENDER::" + string_to_print + "\n"
        actual = buffer.getvalue()
        self.assertEqual(expected, actual)


class TestAPIIntegration(unittest.TestCase):
    def test_api_init(self):
        username = "FOO"
        password = "BAR"
        api = cunyfirstapi.CUNYFirstAPI(username, password)
        self.assertEqual(api._username, username)
        self.assertEqual(api._password, password)

    def test_get_session(self):
        username = "FOO"
        password = "BAR"
        api = cunyfirstapi.CUNYFirstAPI(username, password)
        self.assertIsNotNone(api.get_current_session())

    def test_restart_session(self):
        username = "FOO"
        password = "BAR"
        api = cunyfirstapi.CUNYFirstAPI(username, password)

        first_session = api.get_current_session()
        api.restart_session()
        second_session = api.get_current_session()

        self.assertIsNotNone(first_session)
        self.assertIsNotNone(second_session)
        self.assertNotEqual(first_session, second_session)


    def test_is_logged_in(self):
        username = "FOO"
        password = "BAR"

        api = cunyfirstapi.CUNYFirstAPI(username, password)
        session = api.get_current_session()
        self.assertFalse(api.is_logged_in(session))
        self.assertFalse(api.is_logged_in())
        api.login()

        # Invalid credentials were passed in
        # user should still not be logged in
        self.assertFalse(api.is_logged_in())
        self.assertFalse(api.is_logged_in(session))


def run_test():
    scriptpath = script_path()
    instancepath = instance_path()

    if os.path.isfile(instancepath):
        os.system('rm {0}'.format(instancepath))

    os.system('touch {0}'.format(instancepath))
    unittest.main()
    os.system('rm {0}'.format(instancepath))


def main():
    run_test()


if __name__ == '__main__':
    main()

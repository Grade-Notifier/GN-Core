###********* Imports *********###
from os import sys, path
import os
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from lxml import html
from helper.session import Session, SessionState
from helper import fileManager
from helper import constants

"""login
All login flow happens here
"""

__author__ = "Ehud Adler & Akiva Sherman"
__copyright__ = "Copyright 2018, The Punk Kids"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Ehud Adler & Akiva Sherman"
__email__ = "self@ehudadler.com"
__status__ = "Production"


def logout(session):
    # TODO
    try:
        session.current.get(constants.CUNY_FIRST_LOGOUT_URL)
        session.current.get(constants.CUNY_FIRST_LOGOUT_2_URL)
        session.current.get(constants.CUNY_FIRST_LOGOUT_3_URL)
        return True
    except BaseException:
        return False


def login(session, username, password):
    print('[**] Logging in...')

    session.current.get(constants.CUNY_FIRST_HOME_URL)

    # AUTH LOGIN
    data = {
        'usernameH': '{0}@login.cuny.edu'.format(username),
        'username': username,
        'password': password,
        'submit': ''
    }
    session.current.post(constants.CUNY_FIRST_AUTH_SUBMIT_URL, data=data)

    # STUDENT CENTER
    response = session.current.get(constants.CUNY_FIRST_STUDENT_CENTER_URL)
    tree = html.fromstring(response.text)
    try:
        encquery = tree.xpath('//*[@name="enc_post_data"]/@value')[0]
    except IndexError:
        return False

    data = {'enc_post_data': encquery}
    response = session.current.post(constants.CUNY_FIRST_LOGIN_URL, data=data)

    tree = html.fromstring(response.text)
    try:
        encreply = tree.xpath('//*[@name="enc_post_data"]/@value')[0]
    except IndexError:
        return False
    data = {'enc_post_data': encreply}
    session.current.post(constants.CUNY_FIRST_LOGIN_2_URL, data=data)

    response = session.current.get(
        constants.CUNY_FIRST_SIGNED_IN_STUDENT_CENTER_URL)
    print('[**] Successfully logged in!')
    return True

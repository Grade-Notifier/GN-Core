
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from helper import constants
from helper.helper import get_semester
from bs4 import BeautifulSoup
from lxml import etree
from twilio.rest import Client
from lxml import html
from os.path import join, dirname

"""Cuny Navigator
"""

__author__ = "Ehud Adler & Akiva Sherman"
__copyright__ = "Copyright 2018, The Punk Kids"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Ehud Adler & Akiva Sherman"
__email__ = "self@ehudadler.com"
__status__ = "Production"


'''
The Cuny Navigator makes moving around the cunyFirst website
alot easier.
'''
class CunyNavigator():

    session = None

    def __init__(self, new_session):
        self.session = new_session

    def to_login(self):
        return self.session.get(constants.CUNY_FIRST_HOME_URL)

    def to_student_center(self):
        response = self.session.get(constants.CUNY_FIRST_STUDENT_CENTER_URL)
        tree = html.fromstring(response.text)
        try:
            encquery = tree.xpath('//*[@name="enc_post_data"]/@value')[0]
        except IndexError:
            return False

        data = {'enc_post_data': encquery}
        response = self.session.post(constants.CUNY_FIRST_LOGIN_URL, data=data)

        tree = html.fromstring(response.text)
        try:
            encreply = tree.xpath('//*[@name="enc_post_data"]/@value')[0]
        except IndexError:
            return False
        data = {'enc_post_data': encreply}
        self.session.post(constants.CUNY_FIRST_LOGIN_2_URL, data=data)

        response = self.session.get(
            constants.CUNY_FIRST_SIGNED_IN_STUDENT_CENTER_URL)

    def to_transcript_download(self):
        pass

    def to_current_grade_page(self):
        self.session.get(constants.CUNY_FIRST_GRADES_URL)
        payload = {'ICACTION': 'DERIVED_SSS_SCT_SSS_TERM_LINK'}
        try:
            response = self.session.post(
                constants.CUNY_FIRST_GRADES_URL, data=payload)
        except TimeoutError:
            return None

        tree = html.fromstring(response.text)
        term = helper.get_semester()

        payload_key = ''.join(
            tree.xpath(
                f'//span[text()="{term}"]/parent::div/parent::td/preceding-sibling::td/div/input/@id'))
        payload_value = ''.join(
            tree.xpath(
                f'//span[text()="{term}"]/parent::div/parent::td/preceding-sibling::td/div/input/@value'))
        payload = {
            payload_key: payload_value,
            'ICACTION': 'DERIVED_SSS_SCT_SSR_PB_GO'
        }

        try:
            response = session.current.post(
                constants.CUNY_FIRST_GRADES_URL, data=payload)
            return response
        except TimeoutError:
            return None

    def to_search_classes(self):
        pass

    def to_weekly_schedule(self):
        pass

    def to_exam_schedule(self):
        pass

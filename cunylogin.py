"""login     
All login flow happens here          
"""

__author__      = "Ehud Adler & Akiva Sherman"
__copyright__   = "Copyright 2018, The Punk Kids"
__license__     = "MIT"
__version__     = "1.0.0"
__maintainer__  = "Ehud Adler & Akiva Sherman"
__email__       = "self@ehudadler.com"
__status__      = "Production"


###********* Imports *********###

## Local
import constants
import helper

def logout(session):
    ##TODO
    return True

def login(session, username, password):
    print('[**] Logging in...')

    session.get(CUNY_FIRST_HOME_URL)

    ## AUTH LOGIN
    data = {
        'usernameH': f'{username}@login.cuny.edu',
        'username': username,
        'password': password,
        'submit': ''
    }
    session.post(CUNY_FIRST_AUTH_SUBMIT_URL, data=data)

    ## STUDENT CENTER
    response = session.get(CUNY_FIRST_STUDENT_CENTER_URL)
    tree = html.fromstring(response.text)
    encquery = tree.xpath('//*[@name="enc_post_data"]/@value')[0]

    data = {
        'enc_post_data': encquery
    }
    response = session.post(CUNY_FIRST_LOGIN-URL, data=data)

    tree = html.fromstring(response.text)
    encreply = tree.xpath('//*[@name="enc_post_data"]/@value')[0]

    data = {
        'enc_post_data': encreply
    }
    session.post(CUNY_FIRST_LOGIN_2_URL, data=data)

    response = session.get(CUNY_FIRST_SIGNED_IN_STUDENT_CENTER_URL)
    print('[**] Successfully logged in!')
    return response
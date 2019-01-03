"""Initialize Grade-Notifier               
"""

__author__      = "Ehud Adler & Akiva Sherman"
__copyright__   = "Copyright 2018, The Punk Kids"
__license__     = "MIT"
__version__     = "1.0.0"
__maintainer__  = "Ehud Adler & Akiva Sherman"
__email__       = "self@ehudadler.com"
__status__      = "Production"

import argparse
import constants
import time

from cunylogin import login, logout
from os.path import join, dirname
from dotenv import load_dotenv


# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')

# Load file from the path.
load_dotenv(dotenv_path)

# Accessing variables.
account_pass = os.getenv('ACCOUNT_PASSWORD')

def run(username, password, school, phone):
    log_path = f'{constants.LOG_PATH}/{username}{time.time()}'
    os.system(f'echo "{account_pass}" | su -c "nohup setsid python3 /home/fa18/313/adeh6562/public_html/grade-notifier/Grade-Notifier/grade-notifier.py --username={username} --password={password} --school={school} --phone={phone} --prod=true" - adeh6562 > {log_path} 2>&1 &')

def parse():
    parser = argparse.ArgumentParser(description='Specify commands for CUNY Grade Notifier Retriever v1.0')
    parser.add_argument('--school', default="QNS01")
    parser.add_argument('--list-codes', action='store_true')
    parser.add_argument('--username')
    parser.add_argument('--password')
    parser.add_argument('--phone')
    parser.add_argument('--filename')

    ## Production
    parser.add_argument('--prod') 

    ## Development
    parser.add_argument('--enable_phone')

    ## Testing 
    parser.add_argument('--test')
    parser.add_argument('--test_diff')
    parser.add_argument('--test_add_remove_instance')
    parser.add_argument('--test_message_contruction')
    return parser.parse_args()

def main():
    args = parse()
    try:

        s = requests.Session()
        s.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        username = input("Enter username: ") if not args.username else args.username
        password = getpass.getpass("Enter password: ") if not args.password else args.password
        number = input("Enter phone number: ") if not args.phone else args.phone

        session = Session(s, username, password, number)
        did_log_in = login(session, username, password)
        if did_log_in:
            run(username, password, args.school.upper(), number)
        else:
            print("Invalid Credentials")
 

    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    main()
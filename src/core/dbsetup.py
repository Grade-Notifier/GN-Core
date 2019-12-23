import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_PASSWORD = os.getenv('LOCALHOST_PASSWORD')
ACCOUNT_USERNAME = os.getenv('LOCALHOST_USERNAME')
mydb = mysql.connector.connect(user=ACCOUNT_USERNAME,host='localhost', passwd=ACCOUNT_PASSWORD)
mycursor = mydb.cursor()
mycursor.execute('CREATE DATABASE IF NOT EXISTS GradeNotifier')
mycursor.execute('USE GradeNotifier')
mycursor.execute('CREATE TABLE IF NOT EXISTS Users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255), school VARCHAR(10), gradeHash VARCHAR(255), phoneNumber VARCHAR(255), lastUpdated DATETIME NOT NULL DEFAULT NOW())')

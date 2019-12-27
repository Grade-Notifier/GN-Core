import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv('../../private/.env')

DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_HOST = os.getenv('DB_HOST')
mydb = mysql.connector.connect(user=DB_USERNAME, host=DB_HOST, passwd=DB_PASSWORD)
mycursor = mydb.cursor()
mycursor.execute('CREATE DATABASE IF NOT EXISTS GradeNotifier')
mycursor.execute('USE GradeNotifier')
mycursor.execute('CREATE TABLE IF NOT EXISTS Users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(512), school VARCHAR(10), gradeHash VARCHAR(255), phoneNumber VARCHAR(255), lastChecked DATETIME NOT NULL DEFAULT "1970-01-01 00:00:00", lastUpdated DATETIME NOT NULL DEFAULT "1970-01-01 00:00:00", dateCreated DATETIME NOT NULL DEFAULT NOW())')

from peewee import *
import mysql.connector

import config
from config import *

db = MySQLDatabase(
    database=config.MYSQL_DATABASE,
    host=config.MYSQL_HOST,
    user=config.MYSQL_USER,
    password=config.MYSQL_PASSWORD
)

my_cursor = db.cursor()

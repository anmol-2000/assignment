import logging
import sys
import os
import sqlite3
from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s - %(lineno)d - %(message)s')

def get_db_connection():
    try:
        conn = sqlite3.connect('address_book.db')
        breakpoint()
        cursor = conn.cursor()
        cursor.execute(''' Create Table If Not Exists addresses_book
        (address_id Integer Primary Key AUTOINCREMENT, street Text, city Text, state Text, country Text, latitude Real, longitude Real)''')
        conn.commit()
        return conn
    except Exception as err:
        raise Exception("Not Able to Connect")

def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler

def get_file_handler(log_file):
    file_handler = TimedRotatingFileHandler(log_file, when="midnight", backupCount=3)
    file_handler.setFormatter(FORMATTER)
    return file_handler

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler(f"logs/{logger_name}.log"))
    return logger


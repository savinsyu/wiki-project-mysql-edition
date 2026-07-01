# import sqlite3
# import os.path
#
#
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#
#
# def get_db_connection():
#     db_path = os.path.join(BASE_DIR, '../database.db')
#     conn = sqlite3.connect(db_path, timeout=30)
#     conn.row_factory = sqlite3.Row
#     return conn
#
#
# def close_db_connection(conn):
#     conn.close()

import mysql.connector
from mysql.connector import Error


def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",              # замените на вашего пользователя MySQL
            # password="your_password", # замените на ваш пароль
            database="database"  # замените на имя вашей БД
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Ошибка подключения к MySQL: {e}")
        raise

def close_db_connection(conn):
    if conn and conn.is_connected():
        conn.close()



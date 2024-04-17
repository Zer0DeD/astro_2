import os
import mysql.connector
import locations
import time


class DBHConnection:

    def __init__(self):
        db_host = "localhost"
        db_user = "root"
        db_password = "root"
        db_name = "astro"
        db_port = locations.db_port

        self.dbh = mysql.connector.Connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port)
        self.dbh.autocommit = True

        self.cursor = self.dbh.cursor(buffered=True)

    def cursor_execute(self, sql_request):
        self.cursor.execute(sql_request)
        return self.cursor

    def __del__(self):
        self.cursor.close()
        self.dbh.close()


def cw_start(script_name):
    os.system("echo -------------------------")
    os.system(f"echo {time.asctime()}")
    os.system(f"echo Start of script '{script_name}'")


def cw_finish():
    os.system("echo Completed script execution")
    os.system(f"echo {time.asctime()}")
    os.system("echo -------------------------")


def cw(text):
    os.system(f"echo {text}")

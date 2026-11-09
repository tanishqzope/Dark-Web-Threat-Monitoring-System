import os
import sqlite3
from config import DATABASE_NAME


def monitor_status():
    return True


def database_status():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.close()
        return True
    except:
        return False


def logger_status():
    return os.path.exists(DATABASE_NAME)


def email_status(settings):
    return settings["email_alerts"]


def authentication_status():
    return True


def policy_status():
    return True
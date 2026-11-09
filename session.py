import json
import os

SESSION_FILE = "session.json"


def save_session(username, role):

    data = {
        "username": username,
        "role": role
    }

    with open(
        SESSION_FILE,
        "w"
    ) as file:

        json.dump(data, file)


def load_session():

    if not os.path.exists(SESSION_FILE):

        return None

    with open(
        SESSION_FILE,
        "r"
    ) as file:

        return json.load(file)


def clear_session():

    if os.path.exists(SESSION_FILE):

        os.remove(SESSION_FILE)
#!/bin/python3
# import routes.html_routes

import hashlib
import json
import os
from wsgiref.simple_server import WSGIServer
from data.questions_data import QuestionsData
from data.types.question import Question
import routes.v1.get_run
import routes.v1.get_themes
import routes.v1.new_run


from data.base_data import BaseData
from utils.fs_utils import mkdir_if_not_exist
from utils.startup_utils import load_questions

def main():
    print("Starting up...")
    startup()

    print("Starting webserver")
    http_server = WSGIServer(('', 60218), BaseData.app)
    http_server.serve_forever()

def startup():
    if not os.path.isdir("questions/"):
        raise Exception("Questions folder doesn't exist.")
    if not os.path.isfile("questions/THEMES.json"):
        raise Exception("THEMES.json file doesn't exist.")
    
    mkdir_if_not_exist("runs/")
    # Backup of ended runs
    mkdir_if_not_exist("runs/ended/")
    # Runs not finished & not actively running (eg after 5-10min), should be cleared after a while (eg a week smth like thar)
    mkdir_if_not_exist("runs/idling/")

    load_questions()

if __name__ == "__main__":
    main()

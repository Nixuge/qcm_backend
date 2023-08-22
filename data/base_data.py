from flask import Flask

class BaseData:
    app = Flask(__name__, static_folder="../static")
    MAX_QUESTION_COUNT = 100
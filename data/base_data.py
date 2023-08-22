from flask import Flask

class BaseData:
    app = Flask(__name__, static_folder="../static")
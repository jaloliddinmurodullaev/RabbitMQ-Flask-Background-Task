from flask import Flask

from . import api

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api.blueprint)
    return app
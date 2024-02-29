# shopping_mall/__init__.py
from flask import Flask

# app = Flask(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    return app

# shopping_mall/config.py
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

# MongoDB set up
app.config['MONGO_URI'] = 'mongodb://localhost:27017/shopping_mall'

mongo = PyMongo(app)

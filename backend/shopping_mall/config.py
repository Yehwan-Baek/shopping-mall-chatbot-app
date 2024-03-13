# config.py
from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_jwt_extended import JWTManager
from datetime import timedelta

def create_app():
    app = Flask(__name__)

    # MongoDB setup
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/shopping_mall'
    # jwt setup
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    app.config['JWT_HEADER_TYPE'] = 'Bearer'

    # Connect to MongoDB
    mongo = MongoClient(app.config['MONGO_URI'])
    
    app.mongo = mongo
    # Access the database using mongo['shopping_mall']
    app.db = mongo.shopping_mall

    return app
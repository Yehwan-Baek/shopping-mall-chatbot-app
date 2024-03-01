# models/user.py
from flask import current_app
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
import re

class User:
    # initial model of User
    def __init__(self, email, username, password, user_type=False):
        self.email = email
        self.username = username
        self.password = password
        self.user_type = user_type

    # add email validation logic with regex
    def is_valid_email(self, email):
        email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        return bool(re.match(email_pattern, email))

    # add username validation logic here
    def is_valid_username(self, username):
        return len(username) <=20 and len(username) >= 4
    
    # add password validation logic here
    def is_valid_password(self, password):
        return len(password) <= 14 and len(password) >= 6 

    # matching password from database
    def check_password(self, password):
        return check_password_hash(self.password, password)

    # get jwt athentication
    def get_token(self):
        return create_access_token(identity=self.username)

    # find by username
    @classmethod
    def find_by_username(cls, username):
        users_collection = current_app.mongo.shopping_mall.users
        user_data = users_collection.find_one({'username': username})
        if user_data:
            return cls(
                email=user_data.get('email', ''),
                username=user_data['username'],
                password=user_data['password'],
                user_type=user_data['user_type']
            )
        return None

     # create new user data
    @classmethod
    def create_user(cls, email, username, password, user_type):
        users_collection = current_app.mongo.shopping_mall.users

        # Check for existing username in the database
        existing_user = users_collection.find_one({'username': username})
        if existing_user:
            raise ValueError('Username already exists')

        # Do not hash the password here
        new_user = cls(email=email, username=username, password=password, user_type=False)

        # Validate email
        if not new_user.is_valid_email(email):
            raise ValueError('Invalid email address')

        # Validate username
        if not new_user.is_valid_username(username):
            raise ValueError('Invalid username')

        # Validate password
        if not new_user.is_valid_password(password):
            raise ValueError('Invalid password')

        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(password)
        users_collection.insert_one({
            'username': new_user.username,
            'email': new_user.email,
            'password': hashed_password,
            'user_type': new_user.user_type
        })
        return new_user

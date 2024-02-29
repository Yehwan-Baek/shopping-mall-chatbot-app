# models/user.py
from flask import current_app
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    # initial model of User
    def __init__(self, email, username, password, user_type=False):
        self.email = email
        self.username = username
        self.password = password
        self.user_type = user_type

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
        new_user = cls(email=email, username=username, password=generate_password_hash(passoword), user_type=False)
        users_collection.insert_one({
            'username': new_user.username,
            'email': new_user.email,
            'password': new_user.password,
            'user_type': new_user.user_type
        })
        return new_user
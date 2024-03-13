# routes/user.py
from flask import Blueprint, request, make_response, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from shopping_mall.models.user import User

# set blue print
user_blueprint = Blueprint('user', __name__)

# route to login
@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.find_by_username(username)

    if user and user.check_password(password):
        access_token, refresh_token = user.get_tokens()

        identity = user.username
        return jsonify(access_token=access_token, refresh_token=refresh_token, identity=identity), 200
    else:
        return jsonify(message='Invalid credentials'), 401

# route to refresh access token
@user_blueprint.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    user = User.find_by_username(current_user)

    if user:
        access_token = user.get_tokens()
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message='User not found'), 404

# route to register
@user_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    user_type = data.get('user_type')

    if User.find_by_username(username):
        return jsonify(message='Username already exists'), 400
    new_user = User.create_user(email, username, password, user_type)
    return jsonify(message='User registered successfully', username=new_user.username), 201

# route to logout
@user_blueprint.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Logout logic (if needed)
    return create_response('User logged out successfully')

# route to mypage
@user_blueprint.route('/mypage', methods=['GET'])
def mypage():
    current_user = get_jwt_identity()
    user = User.find_by_username(current_user)

    if user:
        response_data = {'message': 'User found', 'username': user.username}
        response = make_response(jsonify(response_data), 200)
        return response
    else:
        response_data = {'message': 'User not found'}
        response = make_response(jsonify(response_data), 404)
        return response
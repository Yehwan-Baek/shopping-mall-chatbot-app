# routes/user.py
from flask import Blueprint, request, jsonify
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

    print(f"{user.username}")
    print(f"{user.password}")
    print(f"Password check result: {user.check_password(password)}")
    if user and user.check_password(password):
        access_token = user.get_token()
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message='Invalid credentials'), 401

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
@jwt_required()
def mypage():
    current_user = get_jwt_identity()
    user = User.find_by_username(current_user)

    if user:
        return create_response('User found', additional_data={'username': user.username, 'email': user.email})
    else:
        return create_response('User not found', status_code=404)
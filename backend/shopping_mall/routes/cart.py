# routes/cart.py
from flask import Blueprint, request, make_response, jsonify
from shopping_mall.models.cart import CartItem

# set blue print
cart_blueprint = Blueprint('cart',__name__)

# models/cart.py
from flask import current_app

class CartItem:
    def __init__(self, product_id, qty):
        self.product_id = product_id
        self.qty = qty

class ShoppingCart:
    def __init__(self, user_id):
        self.user_id = user_id
        self.items = []

    def add_item(self, product_id, quantity):
        
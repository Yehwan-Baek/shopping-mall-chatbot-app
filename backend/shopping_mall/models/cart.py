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
        existing_item = next((item for item in self.items if item.product_id == product_id), None)

        if existing_item:
            existing_item.quantity += quantity
        else:
            new_item = CartItem(product_id=product_id, quantity=quantity)
            self.items.append(new_item)

    def remove_item(self, product_id):
        self.items = [item for item in self.items if item.product_id != product_id]

    def update_quantity(self, product_id, quantity):
        item = next((item for item in self.items if item.product_id == product_id), None)

        if item:
            item.quantity = quantity

    def clear_cart(self):
        self.items = []

    def calculate_total(self):
        products_collection = current_app.mongo.shopping_mall.products
        total = 0

        for item in self.items:
            product = products_collection.find_one({'_id': ObjectId(item.product_id)})
            if product:
                total += product['price'] * item.quantity

        return total
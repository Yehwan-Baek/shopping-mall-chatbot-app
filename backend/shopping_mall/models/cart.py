# models/cart.py
from flask import current_app
from datetime import datetime
import pytz

class CartItem:
    def __init__(self, product_id, qty):
        self.product_id = product_id
        self.qty = qty

class ShoppingCart:
    def __init__(self, user_id):
        self.user_id = user_id
        self.items = []
        self.creation_date = datetime.now(pytz.timezone("Australia/Sydney"))  # Set creation date in Sydney timezone
        self.status = "Active"
        # another status : "Pending", "Complete", "Cancled", "Expired"

    # find or create cart
    @classmethod
    def find_or_create(cls, user_id):
        # Attempt to find an active shopping cart for the given user_id
        existing_cart = current_app.mongo.shopping_mall.shopping_carts.find_one({
            'user_id': user_id,
            'status': 'Active'
        })

        if existing_cart:
            return cls(user_id=existing_cart['user_id'],
                       items=existing_cart['items'],
                       creation_date=existing_cart['creation_date'],
                       status=existing_cart['status'])

        # If no active cart found, create a new one
        new_cart = cls(user_id=user_id)
        current_app.mongo.shopping_mall.shopping_carts.insert_one(new_cart.to_dict())
        return new_cart

    # set data on dictionary type
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'items': [vars(item) for item in self.items],
            'creation_date': self.creation_date,
            'status': self.status
        }

    # add item in list of cart
    def add_item(self, product_id, quantity):
        existing_item = next((item for item in self.items if item.product_id == product_id), None)

        if existing_item:
            existing_item.quantity += quantity
        else:
            new_item = CartItem(product_id=product_id, quantity=quantity)
            self.items.append(new_item)

    # remove item from list
    def remove_item(self, product_id):
        self.items = [item for item in self.items if item.product_id != product_id]

    # update quantity
    def update_quantity(self, product_id, quantity):
        item = next((item for item in self.items if item.product_id == product_id), None)

        if item:
            item.quantity = quantity

    # remove all in list
    def clear_cart(self):
        self.items = []

    # calculate total price
    def calculate_total(self):
        products_collection = current_app.mongo.shopping_mall.products
        total = 0

        for item in self.items:
            product = products_collection.find_one({'_id': ObjectId(item.product_id)})
            if product:
                total += product['price'] * item.quantity

        return total
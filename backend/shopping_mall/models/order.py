from flask import current_app
from datetime import datetime
import pytz

class OrderItem:
    def __init__(self, product_id, qty):
        self.product_id = product_id
        self.qty = qty

class Order:
    def __init__(self, user_id):
        self.user_id = user_id
        self.items = []
        self.creation_date = datetime.now(pytz.timezone("Australia/Sydney"))  # Set creation date in Sydney timezone
        self.status = "Pending"
        # Status options: "Pending", "Complete", "Cancelled", "Expired"

    # Find or create order
    @classmethod
    def find_or_create(cls, user_id):
        # Attempt to find a pending order for the given user_id
        existing_order = current_app.mongo.shopping_mall.orders.find_one({
            'user_id': user_id,
            'status': 'Pending'
        })

        if existing_order:
            return cls(user_id=existing_order['user_id'],
                       items=existing_order['items'],
                       creation_date=existing_order['creation_date'],
                       status=existing_order['status'])

        # If no pending order found, create a new one
        new_order = cls(user_id=user_id)
        current_app.mongo.shopping_mall.orders.insert_one(new_order.to_dict())
        return new_order

    # Set data on dictionary type
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'items': [vars(item) for item in self.items],
            'creation_date': self.creation_date,
            'status': self.status
        }

    # Add item to order
    def add_item(self, product_id, quantity):
        existing_item = next((item for item in self.items if item.product_id == product_id), None)

        if existing_item:
            existing_item.quantity += quantity
        else:
            new_item = OrderItem(product_id=product_id, quantity=quantity)
            self.items.append(new_item)

    # Remove item from order
    def remove_item(self, product_id):
        self.items = [item for item in self.items if item.product_id != product_id]

    # Update quantity
    def update_quantity(self, product_id, quantity):
        item = next((item for item in self.items if item.product_id == product_id), None)

        if item:
            item.quantity = quantity

    # Clear order
    def clear_order(self):
        self.items = []

    # Calculate total price
    def calculate_total(self):
        products_collection = current_app.mongo.shopping_mall.products
        total = 0

        for item in self.items:
            product = products_collection.find_one({'_id': ObjectId(item.product_id)})
            if product:
                total += product['price'] * item.quantity

        return total

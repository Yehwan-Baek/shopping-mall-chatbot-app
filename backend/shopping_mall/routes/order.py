from flask import Blueprint, request, make_response, jsonify
from shopping_mall.models.order import Order, OrderItem

order_bp = Blueprint('order', __name__)

@order_bp.route('/order', methods=['POST'])
def create_order():
    data = request.json
    user_id = data.get('user_id')
    items = data.get('items')

    # Create a new order
    order = Order(user_id=user_id)

    # Add items to the order
    for item in items:
        product_id = item.get('product_id')
        quantity = item.get('quantity')
        order.add_item(product_id, quantity)

    # Save the order to the database
    current_app.mongo.shopping_mall.orders.insert_one(order.to_dict())

    return jsonify({'message': 'Order created successfully'}), 201

@order_bp.route('/order/<order_id>', methods=['GET'])
def get_order(order_id):
    order_data = current_app.mongo.shopping_mall.orders.find_one({'_id': ObjectId(order_id)})

    if order_data:
        return jsonify(order_data), 200
    else:
        return jsonify({'message': 'Order not found'}), 404

@order_bp.route('/order/<order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.json

    # Find the order
    order_data = current_app.mongo.shopping_mall.orders.find_one({'_id': ObjectId(order_id)})

    if order_data:
        order = Order.find_or_create(order_data['user_id'])

        # Update items in the order
        for item in data.get('items', []):
            product_id = item.get('product_id')
            quantity = item.get('quantity')
            order.update_quantity(product_id, quantity)

        # Save the updated order
        current_app.mongo.shopping_mall.orders.update_one({'_id': ObjectId(order_id)}, {'$set': order.to_dict()})

        return jsonify({'message': 'Order updated successfully'}), 200
    else:
        return jsonify({'message': 'Order not found'}), 404

@order_bp.route('/order/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    # Find and delete the order
    result = current_app.mongo.shopping_mall.orders.delete_one({'_id': ObjectId(order_id)})

    if result.deleted_count == 1:
        return jsonify({'message': 'Order deleted successfully'}), 200
    else:
        return jsonify({'message': 'Order not found'}), 404
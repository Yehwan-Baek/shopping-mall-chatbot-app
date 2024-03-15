from flask import Blueprint, request, make_response, jsonify
from shopping_mall.models.cart import ShoppingCart, CartItem

# Set blueprint
cart_blueprint = Blueprint('cart', __name__)

# route to find cart by user id
@cart_blueprint.route('/cart', methods=['GET'])
def get_cart():
    # Assume the user_id is sent in the request header or as a query parameter
    user_id = request.headers.get('user_id') or request.args.get('user_id')

    if not user_id:
        return make_response(jsonify({'error': 'User ID is required'}), 400)

    # Find or create a shopping cart for the user
    shopping_cart = ShoppingCart.find_or_create(user_id)

    return jsonify(shopping_cart.to_dict()), 200

# route to add items in cart
@cart_blueprint.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.json

    if not data:
        return make_response(jsonify({'error': 'No data provided'}), 400)

    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not product_id or not quantity:
        return make_response(jsonify({'error': 'Product ID and quantity are required'}), 400)

    # Add item to cart
    user_id = request.headers.get('user_id') or request.args.get('user_id')
    if not user_id:
        return make_response(jsonify({'error': 'User ID is required'}), 400)

    shopping_cart = ShoppingCart.find_or_create(user_id)
    shopping_cart.add_item(product_id, quantity)

    return jsonify({'message': 'Item added to cart successfully'}), 200

# route to remove items in cart
@cart_blueprint.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    data = request.json

    if not data:
        return make_response(jsonify({'error': 'No data provided'}), 400)

    product_id = data.get('product_id')

    if not product_id:
        return make_response(jsonify({'error': 'Product ID is required'}), 400)

    # Remove item from cart
    user_id = request.headers.get('user_id') or request.args.get('user_id')
    if not user_id:
        return make_response(jsonify({'error': 'User ID is required'}), 400)

    shopping_cart = ShoppingCart.find_or_create(user_id)
    shopping_cart.remove_item(product_id)

    return jsonify({'message': 'Item removed from cart successfully'}), 200

# route to update quantity of items in cart
@cart_blueprint.route('/cart/update', methods=['POST'])
def update_cart():
    data = request.json

    if not data:
        return make_response(jsonify({'error': 'No data provided'}), 400)

    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not product_id or not quantity:
        return make_response(jsonify({'error': 'Product ID and quantity are required'}), 400)

    # Update item quantity in cart
    user_id = request.headers.get('user_id') or request.args.get('user_id')
    if not user_id:
        return make_response(jsonify({'error': 'User ID is required'}), 400)

    shopping_cart = ShoppingCart.find_or_create(user_id)
    shopping_cart.update_quantity(product_id, quantity)

    return jsonify({'message': 'Cart updated successfully'}), 200

# route to remove cart
@cart_blueprint.route('/cart/clear', methods=['POST'])
def clear_cart():
    # Clear cart
    user_id = request.headers.get('user_id') or request.args.get('user_id')
    if not user_id:
        return make_response(jsonify({'error': 'User ID is required'}), 400)

    shopping_cart = ShoppingCart.find_or_create(user_id)
    shopping_cart.clear_cart()

    return jsonify({'message': 'Cart cleared successfully'}), 200

# route to carculate total price
@cart_blueprint.route('/cart/total', methods=['GET'])
def get_cart_total():
    # Get total price of items in cart
    user_id = request.headers.get('user_id') or request.args.get('user_id')
    if not user_id:
        return make_response(jsonify({'error': 'User ID is required'}), 400)

    shopping_cart = ShoppingCart.find_or_create(user_id)
    total = shopping_cart.calculate_total()

    return jsonify({'total': total}), 200

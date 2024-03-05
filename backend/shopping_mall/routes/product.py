# routes/product.py
from flask import Blueprint, request, make_response, jsonify, render_template
from shopping_mall.models.product import Product

# set blue print
product_blueprint = Blueprint('product',__name__)

# route to find all product
@product_blueprint.route('/', methods=['GET'])
def find_all_products():
    try:
        # retrieve all products
        products = Product.find_all_products()

        return jsonify({"products": products}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# route to create product
@product_blueprint.route('/', methods=['POST'])
def create_product():
    try:
        data = request.get_json()
        name = data.get('name')
        image = data.get('image')
        price = data.get('price')
        qty = data.get('qty')

        if Product.find_by_product_name(name):
            return jsonify(message='Product already exists'), 400
        new_product = Product.create_product(name, image, price, qty)
        return jsonify({"message": "Product created successfully", "product": new_product.__dict__}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
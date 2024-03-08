# routes/product.py
from flask import Blueprint, request, make_response, jsonify
from shopping_mall.models.product import Product

# set blue print
product_blueprint = Blueprint('product',__name__)

# route to find a product detail
@product_blueprint.route('/<string:product_id>', methods=['GET'])
def get_product_detail(product_id):
    try:
        # retrieve product by id
        product = Product.find_by_id(product_id)

        if not product:
            return jsonify(message='Product not found'), 404

        return jsonify({"product": product}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
            return jsonify(message='Product name already exists'), 400
        new_product = Product.create_product(name, image, price, qty)
        return jsonify({"message": "Product created successfully", "product": new_product.__dict__}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# route to update product by id
@product_blueprint.route('/<string:product_id>', methods=['PATCH'])
def update_product(product_id):
    try:
        existing_product = Product.find_by_id(product_id)

        if not existing_product:
            return jsonify(message='Product not found'), 404

        data = request.get_json()
        updated_name = data.get('name', existing_product.name)  # If not provided, keep the existing value
        updated_image = data.get('image', existing_product.image)
        updated_price = data.get('price', existing_product.price)
        updated_qty = data.get('qty', existing_product.qty)

        updated_product = Product.update_product(existing_product, updated_name, updated_image, updated_price, updated_qty)

        return jsonify({"message": "Product updated successfully", "product": updated_product.__dict__}), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
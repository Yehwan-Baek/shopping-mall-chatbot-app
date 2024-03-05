#
from flask import Blueprint, request, make_response, jsonify, render_template
from shopping_mall.models.product import Product

product_blueprint = Blueprint('product',__name__)


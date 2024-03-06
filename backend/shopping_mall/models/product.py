# models/product.py
from flask import current_app

class Product:
    # initial model of Product
    def __init__(self, name, image, price, qty):
        self.name = name
        self.image = image
        self.price = price
        self.qty = qty

    # find all products
    @classmethod
    def find_all_products(cls):
        products_collection = current_app.mongo.shopping_mall.products
        products = list(products_collection.find())

        # Convert ObjectId to string in each product
        for product in products:
            product['_id'] = str(product['_id'])

        return products

    @classmethod
    def find_by_product_name(cls, name):
        products_collection = current_app.mongo.db.product
        product = products_collection.find_one({'name' : name})

    # find by product id
    @classmethod
    def find_by_id(cls, product_id):
        products_collection = current_app.mongo.db.products
        product = products_collection.find_one({'_id' : product_id})
        return product
    
    # create new product data
    @classmethod
    def create_product(cls, name, image, price, qty):
        products_collection = current_app.mongo.shopping_mall.products
        
        existing_product = products_collection.find_one({'name':name})
        if existing_product:
            raise ValueError('Product already exists')

        new_product = cls(name=name, image=image, price=price, qty=qty)

        if price > 0 and qty > 0:
            products_collection.insert_one({
                'name' : name,
                'image' : image,
                'price' : price,
                'qty' : qty
            })
        return new_product

    # update product data
    @classmethod
    def update_product(cls, existing_product, updated_name, updated_image, updated_price, updated_qty):
        products_collection = current_app.mongo.shopping_mall.products

        existing_product.name = updated_name
        existing_product.image = updated_image
        existing_product.price = updated_price
        existing_product.qty = updated_qty

        products_collection.update_one({'_id': existing_product.id}, {'$set': existing_product.__dict__})

        return existing_product
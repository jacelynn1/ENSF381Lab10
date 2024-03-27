from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS 
import json
import os

app = Flask(__name__)
CORS(app)

# create func to read the products data from products.json
def load_products():
    with open('products.json', 'r') as f:
        return json.load(f)['products']
    
# define Flask routes to implement CRUD
#Read (GET) - fetch all products or specific product by ID

@app.route('/products', methods=['GET'])
@app.route('/products/<int:product_id>', methods=['GET'])
def get_products(product_id=None):
    products = load_products()
    if product_id is None:
        # return all products wrapped in an obj w a 'products' key
        return jsonify({"products": products})
    else:
        product = next((p for p in products if p['id'] == product_id), None)
        # if a specific product is requested, wrap it in an obj w a 'product' key
        #Note: might want to change this if u want to return a single product NOT wrapped in a list
        return jsonify(product) if product else ('', 404)

# Create (POST) - add a new product
@app.route('/products/add', methods=['POST'])
def add_product():
    new_product = request.json
    products = load_products()
    new_product['id'] = len(products) + 1
    products.append(new_product)
    with open('products.json', 'w') as f:
        json.dump({"products": products}, f)
    return jsonify(new_product), 201

#IMPLEMENT UPDATE AND DELETE ROUTES HERE
#PUT (UPDATE) - update a product by ID
@app.route('/products/update/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    updated_product = request.json
    products = load_products()
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        product.update(updated_product)
        with open('products.json', 'w') as f:
            json.dump({"products": products}, f)
        return jsonify(product)
    else:
        return ('', 404)

#DELETE (DELETE) - delete a product by ID
@app.route('/products/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    products = load_products()
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        products.remove(product)
        with open('products.json', 'w') as f:
            json.dump({"products": products}, f)
        return ('', 204)
    else:
        return ('', 404)

# Serve images from "product_images" folder
@app.route('/product-images/<path:filename>')
def get_image(filename):
    return send_from_directory('product-images', filename)

# run Flask app including following code at end of server.py
if __name__ == '__main__':
    app.run(debug=True)
from flask import jsonify
from app import app

# Sample products data
products = [
    {"id": 1, "name": "T-Shirt", "category": "Men", "price": 25, "image": ""},
    {"id": 2, "name": "Dress", "category": "Women", "price": 45, "image": ""},
    {"id": 3, "name": "Sneakers", "category": "Men", "price": 60, "image": ""},
    {"id": 4, "name": "Handbag", "category": "Women", "price": 80, "image": ""}

]

# Sample categories
categories = [
    {"id": 1, "name": "Men"},
    {"id": 2, "name": "Women"},
    {"id": 3, "name": "Accessories"}
]

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/categories', methods=['GET'])
def get_categories():
    return jsonify(categories)

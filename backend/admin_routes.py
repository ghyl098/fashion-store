# admin_routes.py
from flask import Blueprint, request, jsonify
from app import db
from models import Admin, Product, Category, Order, Feedback
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# Admin login
@admin_bp.route('/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    admin = Admin.query.filter_by(username=data['username']).first()
    if not admin or not check_password_hash(admin.password, data['password']):
        return jsonify({"msg": "Invalid credentials"}), 401
    token = create_access_token(identity={'id': admin.id, 'is_admin': True})
    return jsonify({"access_token": token, "username": admin.username}), 200

# Add Product
@admin_bp.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    identity = get_jwt_identity()
    if not identity.get('is_admin'):
        return jsonify({"msg": "Unauthorized"}), 403
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'], category_id=data['category_id'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"msg": "Product added"}), 201

# Edit Product
@admin_bp.route('/products/<int:id>', methods=['PUT'])
@jwt_required()
def edit_product(id):
    identity = get_jwt_identity()
    if not identity.get('is_admin'):
        return jsonify({"msg": "Unauthorized"}), 403
    product = Product.query.get_or_404(id)
    data = request.get_json()
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.category_id = data.get('category_id', product.category_id)
    db.session.commit()
    return jsonify({"msg": "Product updated"}), 200

# Delete Product
@admin_bp.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    identity = get_jwt_identity()
    if not identity.get('is_admin'):
        return jsonify({"msg": "Unauthorized"}), 403
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"msg": "Product deleted"}), 200

# View Orders
@admin_bp.route('/orders', methods=['GET'])
@jwt_required()
def view_orders():
    identity = get_jwt_identity()
    if not identity.get('is_admin'):
        return jsonify({"msg": "Unauthorized"}), 403
    orders = Order.query.all()
    result = []
    for o in orders:
        product = Product.query.get(o.product_id)
        user = o.user
        result.append({
            "order_id": o.id,
            "user": user.username,
            "product": product.name,
            "quantity": o.quantity,
            "status": o.status
        })
    return jsonify(result)

# Update Order Status
@admin_bp.route('/orders/<int:id>', methods=['PUT'])
@jwt_required()
def update_order_status(id):
    identity = get_jwt_identity()
    if not identity.get('is_admin'):
        return jsonify({"msg": "Unauthorized"}), 403
    order = Order.query.get_or_404(id)
    data = request.get_json()
    order.status = data.get('status', order.status)
    db.session.commit()
    return jsonify({"msg": "Order status updated"}), 200

# View Feedback
@admin_bp.route('/feedback', methods=['GET'])
@jwt_required()
def view_feedback():
    identity = get_jwt_identity()
    if not identity.get('is_admin'):
        return jsonify({"msg": "Unauthorized"}), 403
    feedbacks = Feedback.query.all()
    result = []
    for f in feedbacks:
        user = f.user
        result.append({"id": f.id, "user": user.username, "message": f.message, "created_at": f.created_at})
    return jsonify(result)

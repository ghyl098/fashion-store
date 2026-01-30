from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

app = Flask(__name__)
CORS(app)

# ---------------------
# Config
# ---------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fashion.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# ---------------------
# Database Models
# ---------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Admin field
    orders = db.relationship('Order', backref='user', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default="Pending")

# ---------------------
# Routes
# ---------------------
@app.route('/')
def home():
    return "Fashion Store Backend is running!"

# ---------------------
# User Routes
# ---------------------
@app.route('/api/users/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "Email already exists"}), 400
    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        username=data['username'], 
        email=data['email'], 
        password=hashed_password,
        is_admin=data.get("is_admin", False)  # Allow admin creation if needed
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201

@app.route('/api/users/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"msg": "Invalid credentials"}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token, "username": user.username, "is_admin": user.is_admin}), 200

# ---------------------
# Category Routes
# ---------------------
@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{"id": c.id, "name": c.name} for c in categories])

# ---------------------
# Product Routes
# ---------------------
@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "price": p.price, "category": p.category.name} for p in products])

@app.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    p = Product.query.get_or_404(id)
    return jsonify({"id": p.id, "name": p.name, "price": p.price, "category": p.category.name})

# Admin-only: Add new product
@app.route('/api/admin/products', methods=['POST'])
@jwt_required()
def add_product():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user.is_admin:
        return jsonify({"msg": "Access denied"}), 403
    data = request.get_json()
    new_product = Product(
        name=data['name'], 
        price=data['price'], 
        category_id=data['category_id']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"msg": "Product added successfully"}), 201

# ---------------------
# Order Routes
# ---------------------
@app.route('/api/orders', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_order = Order(user_id=user_id, product_id=data['product_id'], quantity=data['quantity'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"msg": "Order placed successfully"}), 201

@app.route('/api/orders', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    orders = Order.query.filter_by(user_id=user_id).all() if not user.is_admin else Order.query.all()
    result = []
    for o in orders:
        product = Product.query.get(o.product_id)
        result.append({
            "order_id": o.id,
            "product": product.name,
            "quantity": o.quantity,
            "status": o.status,
            "user": o.user.username
        })
    return jsonify(result)

# ---------------------
# Admin Dashboard Route
# ---------------------
@app.route('/api/admin/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user.is_admin:
        return jsonify({"msg": "Access denied"}), 403
    total_users = User.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    return jsonify({
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders
    })

# ---------------------
# Initialize DB with Sample Data
# ---------------------
def seed_data():
    if not Category.query.first():
        categories = ['Tops', 'Bottoms', 'Outerwear', 'Shoes']
        for c in categories:
            db.session.add(Category(name=c))
        db.session.commit()
    if not Product.query.first():
        products = [
            ("White T-Shirt", 20, 1),
            ("Blue Jeans", 40, 2),
            ("Leather Jacket", 100, 3),
            ("Running Shoes", 60, 4)
        ]
        for name, price, cat_id in products:
            db.session.add(Product(name=name, price=price, category_id=cat_id))
        db.session.commit()
    # Seed admin user
    if not User.query.filter_by(email="admin@example.com").first():
        admin_user = User(
            username="admin",
            email="admin@example.com",
            password=generate_password_hash("admin123"),
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()

# ---------------------
# Run Server
# ---------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(debug=True)

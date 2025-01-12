from flask import Flask, request
from .db import Database

app = Flask(__name__)

database = Database()

@app.route('/')
def home():
    return 'Hello, world'

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        if not username or not password or not role:
            return 'Missing required fields', 400
        if database.register_user(username, password, role):
            return 'User registered successfully', 201
        else:
            return 'Username already exists', 409
    except Exception as e:
        return str(e), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return 'Missing required fields', 400
        if database.login_user(username, password):
            return f'Login as {username} successfully', 200
        else:
            return 'Incorrect username or password', 401
    except Exception as e:
        return str(e), 500
    
@app.route('/add_product', methods=['POST'])
def add_product():
    try:
        data = request.get_json()
        username = data.get('username')
        product_name = data.get('product_name')
        product_price = data.get('product_price')
        product_quantity = data.get('product_quantity')
        product_description = data.get('product_description')
        if not username or not product_name or not product_price or not product_quantity:
            return 'Missing required fields', 400
        if database.add_product(username, product_name, product_price, product_quantity, product_description):
            return f'Product {product_name} added successfully', 201
        else:
            return 'Only sellers can add products', 403
    except Exception as e:
        return str(e), 500
    
@app.route('/remove_product', methods=['DELETE'])
def remove_product():
    try:
        data = request.get_json()
        username = data.get('username')
        product_id = data.get('product_id')
        if not username or not product_id:
            return 'Missing required fields', 400
        if database.remove_product(username, product_id):
            return 'Product removed successfully', 200
        else:
            return f'Product with ID {product_id} not found or not owned by the seller.', 403
    except Exception as e:
        return str(e), 500
    
@app.route('/view_sell_summary', methods=['GET'])
def view_sell_summary():
    try:
        data = request.get_json()
        username = data.get('username')
        if not username:
            return 'Missing required fields', 400
        summary = database.view_sell_summary(username)
        if summary:
            return {'summary': summary}, 200
        else:
            return f'The seller product summary is empty or {username} is not seller', 403
    except Exception as e:
        return str(e), 500
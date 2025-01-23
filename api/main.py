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
        user = database.login_user(username, password)
        if user:
            return {
                'message': f'Login as {username} successfully',
                'user': user.username,
                'role': user.role
            }, 200
        else:
            return 'Incorrect username or password', 401
    except Exception as e:
        return str(e), 500

@app.route('/change_role', methods=['PUT'])
def change_role():
    try:
        data = request.get_json()
        username = data.get('username')
        new_role = data.get('new_role')
        if not username or not new_role:
            return 'Missing required fields', 400
        if database.change_role(username, new_role):
            return f'Role changed to {new_role}', 200
        else:
            return 'User not found', 404
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
        product_image = data.get('product_image')
        if not username or not product_name or not product_price or not product_quantity:
            return 'Missing required fields', 400
        if database.add_product(username, product_name, product_price, product_quantity, product_description, product_image):
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
    
@app.route('/view_seller_summary', methods=['GET'])
def view_seller_summary():
    try:
        data = request.get_json()
        username = data.get('username')
        page = int (data.get('page', 1))
        per_page = int (data.get('per_page', 5))
        if not username:
            return 'Missing required fields', 400
        summary = database.view_seller_summary(username, page, per_page)
        if summary:
            return {'summary': summary}, 200
        else:
            return f'The product schema is empty or {username} is not seller', 403
    except Exception as e:
        return str(e), 500
    
@app.route('/view_order_summary', methods=['GET'])
def view_order_summary():
    try:
        data = request.get_json()   
        username = data.get('username')
        page = int (data.get('page', 1))
        per_page = int (data.get('per_page', 5))
        if not username:
            return 'Missing required fields', 400
        summary = database.view_order_summary(username, page, per_page)
        if summary:
            return {'summary': summary}, 200
        else:
            return f'The product schema is empty', 403
    except Exception as e:
        return str(e), 500
    
@app.route('/add_to_cart', methods=['POST'])    
def add_to_cart():
    try:
        data = request.get_json()
        username = data.get('username')
        product_id = data.get('product_id')
        quantity = int (data.get('quantity'))
        if not username or not product_id or not quantity:
            return 'Missing required fields', 400
        if database.add_to_cart(username, product_id, quantity):
            return 'Product added to cart successfully', 200
        else:
            return 'Product not found or quantity not available', 404
    except Exception as e:
        return str(e), 500
    
@app.route('/view_cart', methods=['GET'])
def view_cart():
    try:
        data = request.get_json()
        username = data.get('username')
        page = int (data.get('page', 1))
        per_page = int (data.get('per_page', 5))
        if not username:
            return 'Missing required fields', 400
        cart = database.view_cart(username, page, per_page)
        if cart:
            return {'cart': cart}, 200
        else:
            return 'Cart is empty', 404
    except Exception as e:
        return str(e), 500
    
@app.route('/checkout', methods=['POST'])
def checkout():
    try:
        data = request.get_json()
        username = data.get('username')
        if not username:
            return 'Missing required fields', 400
        if database.checkout(username):
            return 'Checkout successful', 200
        else:
            return 'Cart is empty', 404
    except Exception as e:
        return str(e), 500
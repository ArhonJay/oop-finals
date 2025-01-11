from flask import Flask, request
from .db import Database

app = Flask(__name__)

database = Database()

@app.route('/')
def home():
    return 'Hello, world'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    database.register_user(username, password)
    return 'User registered successfully', 201

@app.route('/profile')
def profile():
    return 'This is me'
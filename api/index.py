from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return f'Hello, world'

@app.route('/about')
def about():
    return 'This is about'
    
@app.route('/profile')
def profile():
    return 'This is me' 
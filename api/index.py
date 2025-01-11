from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'This is about'
    
@app.route('/profile')
def profile():
    return 'This is me'
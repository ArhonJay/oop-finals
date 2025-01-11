from flask import Flask

app = Flask(__name__)

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f'{self.name} is {self.age} years old'

user = User('John', 30)  

@app.route('/')
def home():
    return f'Hello, {user}'

@app.route('/about')
def about():
    return 'This is about'
    
@app.route('/profile')
def profile():
    return 'This is me' 
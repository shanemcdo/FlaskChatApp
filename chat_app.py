from flask import Flask, redirect, render_template, url_for, session
from flask_socketio import SocketIO, send
from flask_pymongo import PyMongo
from my_secrets import SECRET_KEY, MONGO_URI

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY # randomly generated code
app.config['MONGO_URI'] = MONGO_URI # connection to database
app.config['DEBUG'] = True
io = SocketIO(app)
mongo = PyMongo(app) # get the database

@io.on('message')
def handle_message(data):
    """Handle receiving messages"""
    send(data, broadcast = True)

@app.route('/')
def index():
    """Serve the main page of the website"""
    return render_template('index.html')

@app.route('/login/')
def login():
    """Serve the login page and accept login forms"""
    return render_template('login.html')

@app.route('/signup/')
def signup():
    """Serve the signup page and accept signup forms"""
    return render_template('signup.html')

if __name__ == "__main__": # driver code
    io.run(app)

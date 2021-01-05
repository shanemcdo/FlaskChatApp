from flask import Flask, redirect, render_template, url_for
from flask_socketio import SocketIO, send
from my_secrets import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY # randomly generated code
socketio = SocketIO(app)

@app.route('/')
def index():
    """Serve the main page of the website"""
    return "this is the index"

if __name__ == "__main__": # driver code
    socketio.run(app)

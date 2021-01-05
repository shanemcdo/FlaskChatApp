from flask import Flask, redirect, render_template, url_for
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    """Serve the main page of the website"""
    return "this is the index"

if __name__ == "__main__": # driver code
    socketio.run(app)

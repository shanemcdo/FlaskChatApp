from flask import Flask, redirect, render_template, url_for, session, request
from flask_socketio import SocketIO, send, emit
from flask_pymongo import PyMongo
from my_secrets import SECRET_KEY, MONGO_URI
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY # randomly generated code
app.config['MONGO_URI'] = MONGO_URI # connection to database
app.config['DEBUG'] = True
io = SocketIO(app, manage_session = False)
mongo = PyMongo(app) # get the database

@io.on('connect')
def handle_connect():
    """Handle new connections"""
    print('[[New connection]]', session['username'])
    emit('change_username', session['username'], broadcast = False)
    emit('join_event', session['username'], broadcast = True)

@io.on('disconnect')
def handle_disconnect():
    print('[[Disconnected]]', session['username'])
    emit('leave_event', session['username'], broadcast = True)

@io.on('message')
def handle_message(data):
    """Handle receiving messages"""
    send(data, broadcast = True)

@app.route('/')
def index():
    """Serve the main page of the website"""
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    """Serve the login page and accept login forms"""
    if request.method == 'POST':
        if not request.form['username'] or not request.form['password']:
            return render_template('login.html', error_message = 'Please fill in all information')
        existing_user = mongo.db.users.find_one({'username': request.form['username']})
        if existing_user: # if user already exists
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), existing_user['password']): # if password is correct
                session['username'] = request.form['username']
                return redirect(url_for('index'))
            else: # if password is incorrect
                return render_template('login.html', error_message = 'Password is incorrect')
        else: # if user does not exist
            return render_template('login.html', error_message = 'User does not exist')
    return render_template('login.html')

@app.route('/signup/', methods = ['GET', 'POST'])
def signup():
    """Serve the signup page and accept signup forms"""
    if request.method == 'POST':
        if not request.form['username'] or not request.form['password']:
            return render_template('signup.html', error_message = 'Please fill in all information')
        elif mongo.db.users.find_one({'username': request.form['username']}): # if user already exists
            return render_template('signup.html', error_message = 'Username already taken')
        else: # if user does not exist
            mongo.db.users.insert_one({ # create new user
                'username': request.form['username'],
                'password': bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt()),
                })
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/logout/')
def logout():
    """Log the user out"""
    if 'username' in session:
        del session['username']
    return redirect(url_for('login'))

@app.route('/delete_account/')
def delete_account():
    """Delete the current account"""
    if 'username' in session:
        mongo.db.users.delete_one({'username': session['username']}) # delete current user
        return logout()
    return redirect(url_for('login'))

if __name__ == "__main__": # driver code
    io.run(app, host='0.0.0.0')

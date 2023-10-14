from tv_app import app
from flask import request, render_template, redirect, session, flash
from tv_app.models.loregs import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('loreg_page.html')

@app.route('/create_user', methods=['POST'])
def create_user():
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : request.form['password'],
        'confirm' : request.form['confirm']
    }                                                                              #do not have to have the same amount of data points passing in as the model has for it to go through
    valid = User.validation_user(data)
    if valid:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])           #varchar needs to be 255 characters long in db. especially becuase of the hash
        data['password'] = pw_hash
        User.save(data)
        return redirect('/')
    return redirect('/')

@app.route('/login', methods=['POST'])
def signin():
    data = {
        'email' : request.form['email'],
        'password' : request.form['password'] 
    }
    user = User.get_email(data)
    if not user:
        flash('Invalid email or password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid email or password', 'login')
        return redirect('/')
    id = User.get_id(data)
    session['user_id'] = id.user_id
    return redirect('/dashboard')
    
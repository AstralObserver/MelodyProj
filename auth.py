from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint('auth', __name__)

# Signup Route
@auth_bp.route('/signup', methods=['POST', 'GET'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            error = 'Username and password are required'
            return render_template('signup.html', error=error)

        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            error = 'Username already exists'
            return render_template('signup.html', error=error)

        # Create a new user instance
        new_user = User(username=username)
        new_user.set_password(password)  # Set the hashed password

        # Save the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Log the user in and redirect to the main page or dashboard
        login_user(new_user)
        return redirect(url_for('userpage'))  # Assuming you have a main blueprint with an index route

    return render_template('signup.html', error=error)

# Login Route
@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('auth.profile', username=user.username))  # Redirect to index after login
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)

# Logout Route
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Profile Route
@auth_bp.route('/User/<username>')
@login_required
def profile(username):
    return render_template('userpage.html', username=username)
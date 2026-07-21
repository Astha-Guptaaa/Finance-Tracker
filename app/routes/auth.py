# Authentication Routes
# Author: Senior Software Engineering Mentor

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app.models.user import User
from app.database import get_db_connection
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    """
    Decorator to protect routes that require authentication.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration.
    """
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check Database Connection First
        if not get_db_connection():
            flash('Database connection failed. Please check your .env file and restart the server.', 'danger')
        # Basic Validation
        elif not username or not email or not password:
            flash('All fields are required.', 'danger')
        elif password != confirm_password:
            flash('Passwords do not match.', 'danger')
        elif User.get_by_username(username):
            flash('Username already exists.', 'danger')
        elif User.get_by_email(email):
            flash('Email already registered.', 'danger')
        else:
            # Create User
            user_id = User.create(username, email, password)
            if user_id:
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('An error occurred during registration.', 'danger')

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login and session creation.
    """
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.get_by_username(username)

        if user and User.verify_password(user['password_hash'], password):
            session.permanent = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """
    Handles user logout and session clearance.
    """
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

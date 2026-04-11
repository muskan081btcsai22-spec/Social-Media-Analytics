from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from bson.objectid import ObjectId

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    from flask import current_app as app
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app.db.users.find_one({'username': username}):
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.register'))
        pw_hash = generate_password_hash(password)
        user = {'username': username, 'password_hash': pw_hash, 'created_at': __import__('datetime').datetime.utcnow()}
        res = app.db.users.insert_one(user)
        flash('Registered. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    from flask import current_app as app
    from app.models.user import User
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        data = app.db.users.find_one({'username': username})
        if not data:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        if check_password_hash(data.get('password_hash', ''), password):
            user = User(data)
            login_user(user)
            flash('Logged in', 'success')
            return redirect(url_for('cases.dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('auth.login'))

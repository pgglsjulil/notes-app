from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import User
from app import db
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)


@main.route('/')
def landing_page():
    return render_template('landing_page.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'GET':
        return render_template('register.html')

    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()
    if existing_user:
        flash('Username or email already exists.', 'danger')
        return redirect(url_for('main.register'))

    new_user = User(
        username=username, password=generate_password_hash(password), email=email
    )
    db.session.add(new_user)
    db.session.commit()

    flash('Registration successful! Please log in.', 'success')
    return redirect(url_for('main.login'))


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()
    if not user:
        flash('Invalid email or password.', 'danger')
        return redirect(url_for('main.login'))

    if not check_password_hash(user.password, password):
        flash('Invalid email or password.', 'danger')
        return redirect(url_for('main.login'))

    login_user(user)
    flash('Login successful!', 'success')
    return redirect(url_for('main.home'))


@main.route('/home', methods=['GET'])
def home():
    if not current_user.is_authenticated:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('main.login'))

    return render_template('home.html')

@main.route('/catatan')
def catatan():
    return render_template('catatan.html')

@main.route('/home_kemynotes')
def home_kemynotes():
    return render_template('home_kemynotes.html')

# @main.route('/show-mynotes')
# def show_mynotes():
#     return redirect(url_for('home', view='show-mynotes'))


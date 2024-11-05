# auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from datetime import datetime

auth = Blueprint('auth', __name__)

# @auth.route('/sign-up', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         first_name = request.form.get('first_name')
#         last_name = request.form.get('last_name')
#         email = request.form.get('email')
#         phone_number = request.form.get('phone_number')
#         address = request.form.get('address')
#         role = request.form.get('role')
#         password = request.form.get('password')
#         gender = request.form.get('gender')

#         # Check if user exists
#         user = User.query.filter_by(email=email).first()
#         if user:
#             flash('Email already exists.', 'error')
#             return redirect(url_for('auth.register'))

#         # Create a new user with a hashed password
#         new_user = User(
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             phone_number=phone_number,
#             address=address,
#             role=role,
#             password_hash=generate_password_hash(password, method='sha256'),
#             gender=gender,
#             date_registered=datetime.utcnow()
#         )

#         db.session.add(new_user)
#         db.session.commit()
#         flash('Registration successful!', 'success')
#         return redirect(url_for('auth.login'))

#     return render_template('sign-up.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Find user by email
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            user.last_login = datetime.utcnow()
            db.session.commit()
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login failed. Check your email or password.', 'error')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

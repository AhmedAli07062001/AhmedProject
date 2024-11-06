from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from . import db  # Ensure you import db for database operations
from .models import User  # Import your User model
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Query user by email
        user = User.query.filter_by(email=email).first()

        # Check if the user exists and password matches
        if user and user.check_password(password):
            session['email'] = user.email
            flash('Login Successful', 'success')
            return redirect(url_for('auth.dashboard'))
        
        else:
            flash('Email or Password is Incorrect', 'error')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # Get the form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')
        role = request.form.get('role')
        gender = request.form.get('gender')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("Passwords do not match, please try again.", "error")
            return redirect(url_for('sign_up'))  # Reload the page


        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please use a different email.', 'error')
            return redirect(url_for('auth.sign_up'))
        
        if not gender:
            flash('Please select your gender.', 'error')
            return redirect(url_for('auth.sign_up'))
        
        # Create a new user instance
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            address=address,
            role=role,
            gender=gender,
            password_hash=generate_password_hash(password)  # Make sure to import and use this function
        )

        # Add and commit the new user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('You have successfully registered!', 'success')
            return redirect(url_for('login'))
        except:
            flash('Error occurred during registration.', 'error')
            db.session.rollback()

    return render_template('signup.html')

@auth.route('/dashboard')
def dashboard():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html', user=user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

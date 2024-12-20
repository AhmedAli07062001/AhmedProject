from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta, timezone
from app.models import User
from app.utils import send_otp_email  # Helper function moved to utils.py
from app import db
import random

auth_bp = Blueprint('auth', __name__)

# Routes login 
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            session['email'] = user.email
            flash('Login Successful', 'success')
            return redirect(url_for('auth.dashboard'))  # Update with appropriate dashboard
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html')

#route sign up
@auth_bp.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')
        gender = request.form.get('gender')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        birthdate = request.form.get('birthdate')  # Ensure this field exists in your form

        if password != confirm_password:
            flash("Passwords do not match.", 'error')
            return redirect(url_for('auth.sign_up'))

        if User.query.filter_by(email=email).first():
            flash("Email is already registered.", 'error')
            return redirect(url_for('auth.sign_up'))

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            address=address,
            gender=gender,
            password_hash=generate_password_hash(password),
            birthdate=birthdate
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully.", 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred during registration.", 'error')
            print(f"Error: {e}")
            return redirect(url_for('auth.sign_up'))

    return render_template('auth/signup.html')

#route forget password
@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("This email is not registered.", 'error')
            return redirect(url_for('auth.forgot_password'))

        otp = random.randint(100000, 999999)
        session['otp'] = otp
        session['otp_expiry'] = datetime.now(timezone.utc) + timedelta(minutes=5)
        session['email'] = email

        try:
            send_otp_email(email, otp)
            flash("OTP sent to your email.", 'success')
            return redirect(url_for('auth.otp_verification'))
        except Exception as e:
            flash("Failed to send OTP. Try again.", 'error')
            print(f"Error: {e}")
            return redirect(url_for('auth.forgot_password'))

    return render_template('auth/forgot_password.html')


# otp verification
@auth_bp.route('/otp-verification', methods=['GET', 'POST'])
def otp_verification():
    if request.method == 'POST':
        entered_otp = ''.join(request.form.get(f'otp_digit_{i}') for i in range(1, 7))
        if session.get('otp') and session.get('otp_expiry') >= datetime.now(timezone.utc):
            if str(session['otp']) == entered_otp:
                session.pop('otp', None)
                session.pop('otp_expiry', None)
                return redirect(url_for('auth.new_password'))
            else:
                flash("Invalid OTP. Try again.", 'error')
        else:
            flash("OTP expired. Request a new one.", 'warning')
            return redirect(url_for('auth.forgot_password'))

    return render_template('auth/otp_verification.html')

# new password
@auth_bp.route('/new-password', methods=['GET', 'POST'])
def new_password():
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("Passwords do not match.", 'error')
            return redirect(url_for('auth.new_password'))

        user = User.query.filter_by(email=session.get('email')).first()
        if not user:
            flash("Session expired. Please try again.", 'error')
            return redirect(url_for('auth.forgot_password'))

        try:
            user.password_hash = generate_password_hash(password)
            db.session.commit()
            flash("Password reset successfully. Please log in.", 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash("Error resetting password.", 'error')
            print(f"Error: {e}")
            return redirect(url_for('auth.new_password'))

    return render_template('auth/new_password.html')

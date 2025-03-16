from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta, timezone
from app.models import User
from app.utils import send_otp_email 
from app import db
import random
import re
import logging

auth_bp = Blueprint('auth', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html',active_page='login')

#route sign up
@auth_bp.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form.get('first_name').strip()
        last_name = request.form.get('last_name').strip()
        age = request.form.get('age').strip()
        gender = request.form.get('gender')
        email = request.form.get('email').strip()
        phone_number = request.form.get('phone_number').strip()
        state = request.form.get('state', '').strip()
        city = request.form.get('city', '').strip()
        role = request.form.get('role') # Admin, Therapist, Patient
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Email already exists check
        user = User.query.filter_by(email=email).first()
        if user:
            flash('❌ Email already exists. Please use a different email.', 'danger')
            return redirect(url_for('auth.sign_up'))

        # Password match check
        if password != confirm_password:
            flash('❌ Passwords do not match.', 'danger')
            return redirect(url_for('auth.sign_up'))

        # Basic validations
        if not first_name or not last_name:
            flash("First name and last name are required.", 'danger')
            return redirect(url_for('auth.sign_up'))

        if not age.isdigit() or int(age) <= 0:
            flash("Invalid age. Please enter a valid number.", 'danger')
            return redirect(url_for('auth.sign_up'))

        if gender not in ['male', 'female', 'other']:
            flash("Please select a valid gender.", 'danger')
            return redirect(url_for('auth.sign_up'))

        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format.", 'danger')
            return redirect(url_for('auth.sign_up'))

        if not phone_number.isdigit() or len(phone_number) != 10:
            flash("Invalid phone number. It should be 10 digits.", 'danger')
            return redirect(url_for('auth.sign_up'))

        if not password or len(password) < 8 or not re.search(r"[A-Za-z0-9@#$%^&+=]", password):
            flash("Password must be at least 8 characters long and contain letters, numbers, and special characters.", 'danger')
            return redirect(url_for('auth.sign_up'))

        # Create new user
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            age=int(age),
            gender=gender,
            email=email,
            phone_number=phone_number,
            state=state,
            city=city,
            role=role,
            password_hash=generate_password_hash(password)
            
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully! You can now log in.", 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error adding user to the database: {e}")
            flash("An error occurred during registration. Please try again later.", 'danger')
            return redirect(url_for('auth.sign_up'))

    return render_template('auth/signup.html', active_page='sign_up')

#route forget password
@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("This email is not registered.", 'danger')
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
            flash("Failed to send OTP. Try again.", 'danger')
            print(f"Error: {e}")
            return redirect(url_for('auth.forgot_password'))

    return render_template('auth/forget password.html')

#route otp verification
@auth_bp.route('/otp_verification', methods=['GET', 'POST'])
def otp_verification():
    if request.method == 'POST':
        otp = ''.join([request.form.get(f'otp_digit_{i}') for i in range(1, 7)])  # Collect all digits
        if 'otp' not in session or session['otp'] != int(otp):
            flash("Invalid OTP.", 'error')
            return redirect(url_for('auth.otp_verification'))

        if datetime.now(timezone.utc) > session['otp_expiry']:
            flash("OTP expired.", 'error')
            return redirect(url_for('auth.forgot_password'))

        flash("OTP verified. You can now reset your password.", 'success')
        return redirect(url_for('auth.new_password'))

    return render_template('auth/OTP Verification.html')

@auth_bp.route('/resend_otp', methods=['GET'])
def resend_otp():
    if 'email' not in session:
        flash("Session expired. Please try again.", 'error')
        return redirect(url_for('auth.forgot_password'))

    try:
        otp = random.randint(100000, 999999)
        session['otp'] = otp
        session['otp_expiry'] = datetime.now(timezone.utc) + timedelta(minutes=5)

        send_otp_email(session['email'], otp)
        flash("OTP resent to your email.", 'success')
    except Exception as e:
        flash("Failed to resend OTP. Please try again.", 'error')
        print(f"Error: {e}")

    return redirect(url_for('auth.otp_verification'))

#route new password
@auth_bp.route('/new_password', methods=['GET', 'POST'])
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

    return render_template('auth/new password.html')
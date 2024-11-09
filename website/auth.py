from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from . import db  # Ensure you import db for database operations
from .models import User  # Import your User model
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash
import random
from datetime import datetime, timedelta, timezone
from flask_mail import Message
from . import mail
import socket

auth = Blueprint('auth', __name__)

# Route for login
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

# Route for signing up
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
            return redirect(url_for('auth.sign_up'))  # Reload the page

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
            return redirect(url_for('auth.login'))
        except:
            flash('Error occurred during registration.', 'error')
            db.session.rollback()

    return render_template('signup.html')

# Route for dashboard
@auth.route('/dashboard')
def dashboard():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        if user:
            return render_template('dashboard.html', user=user)
        else:
            flash("User not found", "error")
            return redirect(url_for('auth.login'))  # Redirect if user is not found
    else:
        flash("You are not logged in", "error")
        return redirect(url_for('auth.login'))

# Route for logging out
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Route for Forgot Password
@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')

        # Check if the email exists in the database
        user = User.query.filter_by(email=email).first()
        if user:
            session['email'] = email  # Store email in session
            flash('An OTP has been sent to your email address. Please verify to reset your password.', 'success')
            return redirect(url_for('auth.send_otp'))  # Send OTP instead of redirecting directly to OTP verification page
        else:
            # Flash an error message if email does not exist
            flash('This email is not registered. Please check the email and try again.', 'error')
            return redirect(url_for('auth.forgot_password'))  # Redirect back to forgot password page

    return render_template('forget password.html')  # Render the forgot password page

# Route for sending the random OTP
@auth.route('/send_otp')
def send_otp():
    email = session.get('email')
    if not email:
        flash('Session expired. Please try again.', 'error')
        return redirect(url_for('auth.forgot_password'))  # Redirect to forgot password page

    otp = random.randint(100000, 999999)
    session['otp'] = otp
    session['otp_expiry'] = datetime.now(timezone.utc) + timedelta(minutes=5)

    try:
        send_otp_email(email, otp)  # Send OTP to the user's email
        flash(f"An OTP has been sent to {email}. Please verify.", "info")  # Flash message
    except socket.gaierror:
        flash("Failed to send OTP: Internet connection issue. Please try again.", "error")
        return redirect(url_for('auth.forgot_password'))
    except Exception as e:
        flash(f"Failed to send OTP due to technical issue.", "error")
        return redirect(url_for('auth.forgot_password'))

    return redirect(url_for('auth.otp_verification'))

def send_otp_email(to_email, otp):
    msg = Message("Your OTP for Password Reset", recipients=[to_email])
    msg.body = f"Your OTP is {otp}. Please use this to reset your password."
    mail.send(msg)

# Route for OTP verification page
@auth.route('/otp_verification')
def otp_verification():
    return render_template('OTP Verification.html')

# Route for verifying the OTP
@auth.route('/verify_otp', methods=['POST'])
def verify_otp():
    otp_digits = [request.form.get(f'otp_digit_{i}') for i in range(1, 7)]
    entered_otp = ''.join(otp_digits)
    stored_otp = session.get('otp')
    expiry_time = session.get('otp_expiry')
    
    if stored_otp and datetime.now(timezone.utc) <= expiry_time:
        if str(stored_otp) == entered_otp:
            flash('OTP verified successfully!', 'success')
            session.pop('otp', None)
            session.pop('otp_expiry', None)
            return render_template('new password.html')
        else:
            flash('Invalid OTP. Please try again.', 'error')
    else:
        flash("OTP has expired. Please request a new one.", "warning")
    return redirect(url_for('auth.otp_verification'))

# Route for resending the OTP
@auth.route('/resend_otp')
def resend_otp():
    return send_otp()

# Route for setting the new password
@auth.route('/new-password', methods=['GET', 'POST'])
def new_password():
    if request.method == 'POST':
        # Get the new password and confirm password from the form
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for('auth.new_password'))

        # Get user from session (or if using OTP, from a token, etc.)
        user_email = session.get('email')  # Assuming the email is stored in session after OTP verification
        if not user_email:
            flash("Session expired, please try again.", "error")
            return redirect(url_for('auth.login'))

        # Find the user in the database
        user = User.query.filter_by(email=user_email).first()
        if user:
            # Hash the new password
            user.password_hash = generate_password_hash(password)
            
            try:
                db.session.commit()  # Save the new password to the database
                flash("Password has been updated successfully.", "success")
                return redirect(url_for('auth.login'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred while updating the password: {str(e)}", "error")
                return redirect(url_for('auth.new_password'))
        else:
            flash("User not found.", "error")
            return redirect(url_for('auth.login'))

    return render_template('new password.html')  # Render the 'new password' page

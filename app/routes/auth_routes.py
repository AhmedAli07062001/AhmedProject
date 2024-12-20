from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return render_template('auth/login.html')

@auth_bp.route('/sign-up')
def sign_up():
    return render_template('auth/signup.html')

@auth_bp.route('/forgot-password')
def forgot_password():
    return render_template('auth/forget password.html')

@auth_bp.route('/OTP-Verification')
def otp_verification():
    return render_template('auth/OTP Verification.html')

@auth_bp.route('/New-Password')
def new_password():
    return render_template('auth/new password.html')

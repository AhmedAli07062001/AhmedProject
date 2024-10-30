from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dont try to cheat my secret key its impossible'


    # Route for the home page
    @app.route('/')
    def home():
        return render_template('index.html')  # Render the home page
    
    @app.route('/login')
    def login():
        return render_template('login.html')   #render to the login page
    
    @app.route('/sign-up')
    def sign_up():
        return render_template('signup.html')  #render to the sign-up page
    
    @app.route('/OTP-Verification')
    def opt_verification():
        return render_template('OTP Verification.html')   #render to the opt verification page

    @app.route('/New-Password')
    def new_password():
        return render_template('new password.html')   

    return app

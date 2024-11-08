from flask import Flask, render_template  # Ensure this is included
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

# Initialize the SQLAlchemy object
db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dont try to cheat my secret key its impossible'

    # Uncomment this when setting up the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ahmed#2909@localhost/SpeechCareHub'
    
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Example for Gmail
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'ahmedali29090067@gmail.com'
    app.config['MAIL_PASSWORD'] = 'ymyc upwv zdqs ixtr'
    app.config['MAIL_DEFAULT_SENDER'] = 'ahmed.ali.404716@gmail.com'
    
    mail.init_app(app)

    # Initialize the database
    db.init_app(app)
    
    # Register blueprints (uncomment when using auth blueprint)
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')
    
    # Create tables if they don’t exist (uncomment for database setup)
    with app.app_context():
        db.create_all()

    # Route for the home page
    @app.route('/')
    def home():
        print("Home page accessed")
        return render_template('index.html')  # Render the home page
    
    @app.route('/login')
    def login():
        return render_template('login.html')  # Render the login page
    
    @app.route('/sign-up')
    def sign_up():
        return render_template('signup.html')  # Render the sign-up page
    
    @app.route('/forgot_password')
    def forgot_password():
        return render_template('forget password.html') #render to forgot password

    @app.route('/OTP-Verification')
    def otp_verification():
        return render_template('OTP Verification.html')  # Render the OTP verification page

    @app.route('/New-Password')
    def new_password():
        return render_template('new password.html')  # Render the new password page
    
    @app.route('/chatbot')
    def chatbot():
        return render_template('chatbot.html')  # Render the chatbot page

    return app

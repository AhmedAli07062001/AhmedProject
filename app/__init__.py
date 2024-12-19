from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

# Initialize the extensions
db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'dont try to cheat my secret key its impossible'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ahmed#2909@localhost/SpeechCareHub'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'ahmedali29090067@gmail.com'
    app.config['MAIL_PASSWORD'] = 'ymyc upwv zdqs ixtr'
    app.config['MAIL_DEFAULT_SENDER'] = 'ahmed.ali.408716@gmail.com'

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)

    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.patient_routes import patient_bp
    from app.routes.therapist_routes import therapist_bp
    from app.routes.appointment_routes import appointment_bp
    from app.routes.general_routes import general_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(patient_bp, url_prefix='/patient')
    app.register_blueprint(therapist_bp, url_prefix='/therapist')
    app.register_blueprint(appointment_bp, url_prefix='/appointment')
    app.register_blueprint(general_bp)

    # Initialize database
    with app.app_context():
        db.create_all()

    return app

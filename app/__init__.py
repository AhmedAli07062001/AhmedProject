from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import Config

# Initialize the extensions
db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)

    # Load configuration from Config class
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)

    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.patient_routes import patient_bp
    from app.routes.therapist_routes import therapist_bp
    from app.routes.appointment_routes import appointment_bp
    from app.routes.general_routes import general_bp
    from app.errors.handlers import errors_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(patient_bp, url_prefix='/patient')
    app.register_blueprint(therapist_bp, url_prefix='/therapist')
    app.register_blueprint(appointment_bp, url_prefix='/appointment')
    app.register_blueprint(general_bp)
    app.register_blueprint(errors_bp)

    # Initialize database
    with app.app_context():
        db.create_all()

    return app

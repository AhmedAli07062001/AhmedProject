from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Enum
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db  # Import db from extensions.py

class User(db.Model, UserMixin):
    __tablename__ = 'User'

    user_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(Enum('Male', 'Female'), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(10), unique=True, nullable=False)
    state = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    role = db.Column(Enum('Admin', 'Therapist', 'Patient'), default='Patient', nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    date_registered = db.Column(db.DateTime, default=func.current_timestamp())
    last_login = db.Column(db.DateTime, nullable=True)
    last_updated = db.Column(db.DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    def get_id(self):
        """Flask-Login ko user ka unique ID string format me chahiye."""
        return str(self.user_id)

    def set_password(self, password):
        """Hashes password and stores securely."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifies password with stored hash."""
        return check_password_hash(self.password_hash, password)

from flask_login import UserMixin
from sqlalchemy import Enum
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db  # Import db from extensions.py
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'patient' or 'therapist'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = db.relationship('Patient', backref='user', uselist=False, cascade='all, delete-orphan')
    therapist = db.relationship('Therapist', backref='user', uselist=False, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50), nullable=False)  # 'male' or 'female'
    phone_number = db.Column(db.String(15), nullable=False)
    state = db.Column(db.String(255))
    city = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Therapist(db.Model):
    __tablename__ = 'therapists'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    state = db.Column(db.String(255))
    city = db.Column(db.String(255))
    designation = db.Column(db.String(255))  # Add this line
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
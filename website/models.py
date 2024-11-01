# models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, 
                     check_constraint="role IN ('Patient', 'Therapist', 'Supervisor', 'Admin')")
    profile_pic = db.Column(db.String(255), nullable=True)
    date_registered = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    last_login = db.Column(db.Date, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    last_updated = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.email}>'

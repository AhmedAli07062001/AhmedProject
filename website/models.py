from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash

# Import db object
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(50), nullable=False,default='Patient')
    profile_pic = db.Column(db.String(255))
    date_registered = db.Column(db.Date, nullable=False,default=db.func.current_date())
    last_login = db.Column(db.Date)
    password_hash = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    last_updated = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now())

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.user_id

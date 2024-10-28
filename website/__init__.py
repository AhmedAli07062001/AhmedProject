from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dfkjdkfd fjkdfdjkfjdkd fddfdd'


    # Route for the home page
    @app.route('/')
    def home():
        return render_template('index.html')  # Render the home page

    return app

from flask import Blueprint, render_template

general_bp = Blueprint('general', __name__)

@general_bp.route('/')
def home():
    return render_template('general/index.html')

@general_bp.route('/chatbot')
def chatbot():
    return render_template('general/chatbot.html')

@general_bp.route('/contact')
def contact():
    return render_template('general/contact.html')

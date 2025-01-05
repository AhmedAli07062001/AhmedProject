from flask import Blueprint, render_template,request, redirect, url_for, flash, current_app
from flask_mail import Message
from .. import mail

general_bp = Blueprint('general', __name__)

@general_bp.route('/')
def home():
    return render_template('general/index.html')

@general_bp.route('/chatbot')
def chatbot():
    return render_template('general/chatbot.html',active_page='chatbot')

@general_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Server-side validation
        if not name or not email or not message:
            flash('All fields are required!', 'error')
            return redirect(url_for('general.contact'))

        # Flash message confirmation
        flash('Message sent successfully!', 'success')

        # Optional: Send an email with Flask-Mail
        msg = Message('New Contact Form Submission',
                      sender=current_app.config['MAIL_USERNAME'],
                      recipients=['ahmedali29090067@gmail.com'])
        msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        mail.send(msg)

        return redirect(url_for('general.contact'))

    return render_template('general/contact.html')

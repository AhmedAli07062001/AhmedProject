from flask import Blueprint, render_template

therapist_bp = Blueprint('therapist', __name__)

@therapist_bp.route('/dashboard')
def doctor_dashboard():
    return render_template('therapist/doctor_dashboard.html')

@therapist_bp.route('/list')
def doctor_list():
    return render_template('therapist/doctor_list.html')

@therapist_bp.route('/card')
def doctor_card():
    return render_template('therapist/doctor_card.html')

@therapist_bp.route('/profile')
def doctor_profile():
    return render_template('therapist/doctor_profile.html')

@therapist_bp.route('/add')
def add_doctor():
    return render_template('therapist/add_doctor.html')

@therapist_bp.route('/edit')
def edit_doctor():
    return render_template('therapist/edit_doctor.html')

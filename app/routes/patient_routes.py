from flask import Blueprint, render_template

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/dashboard')
def patient_dashboard():
    return render_template('patient/patient_dashboard.html')

@patient_bp.route('/edit')
def edit_patient():
    return render_template('patient/edit_patient.html')

@patient_bp.route('/add')
def add_patient():
    return render_template('patient/add_patient.html')

@patient_bp.route('/list')
def patient_list():
    return render_template('patient/patient_list.html')

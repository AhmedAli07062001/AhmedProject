from flask import Blueprint, render_template, flash, redirect, url_for,session,request
from app.models import User

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/User/<int:id>')
def patient_profile(id):
    if 'email' not in session:
        flash("You are not logged in", "error")
        return redirect(url_for('auth.login'))

    user_profile = User.query.get(id)
    if not user_profile:
        flash("User not found.", "error")
        return redirect(url_for('auth.login'))

    return render_template('patient/patient_dashboard.html', user_profile=user_profile)



# Route for patinet dashboard
@patient_bp.route('/patient_dashboard')
def patient_dashboard():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        if user:
            return render_template('patient/patient_dashboard.html', user_profile=user)
        else:
            flash("User not found", "error")
            return redirect(url_for('auth.login'))  # Redirect if user is not found
    else:
        flash("You are not logged in", "error")
        return redirect(url_for('auth.login'))


@patient_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    patient = User.query.get(id)
    if request.method == 'POST':
        # Logic to update patient info
        pass
    return render_template('patient/edit_patient.html', patient=patient)


@patient_bp.route('/add')
def add_patient():
    return render_template('patient/add_patient.html')

@patient_bp.route('/list')
def patient_list():
    return render_template('patient/patient_list.html')



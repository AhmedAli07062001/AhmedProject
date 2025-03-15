from flask import Blueprint, render_template, flash, redirect, url_for,session,request
from app.models import User

admin_bp = Blueprint('admin', __name__)

# Route for patinet dashboard
@admin_bp.route('/admin_dashboard')
def admin_dashboard():
    if 'email' in session:
        patient = User.query.filter_by(email=session['email']).first()
        if patient:
            return render_template('admin/admin_dashboard.html',active_page='admin_dashboard')
        else:
            flash("User not found", "error")
            return redirect(url_for('auth.login'))  # Redirect if user is not found
    else:
        flash("You are not logged in", "error")
        return redirect(url_for('auth.login'))
    

@admin_bp.route('/add_doctor')
def add_doctor():
    return render_template('admin/add_doctor.html',active_page='add_doctor')

@admin_bp.route('/edit_user')
def edit_user():
    return render_template('admin/edit_user.html',active_page='edit_user')

@admin_bp.route('/edit_doctor')
def edit_doctor():
    return render_template('admin/edit_doctor.html',active_page='edit_doctor')
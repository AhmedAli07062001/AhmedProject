from flask import Blueprint, render_template, flash, redirect, url_for,session,request
from app.models import User

therapist_bp = Blueprint('therapist', __name__)

@therapist_bp.route('/dashboard')
def therapist_dashboard():
    if 'email' in session:
        therapist = User.query.filter_by(email=session['email']).first()
        if therapist:
            return render_template('therapist/therapist_dashboard.html', user_profile=therapist,active_page='therapist_dashboard')
        else:
            flash("User not found", "error")
            return redirect(url_for('auth.login'))
    else:
        flash("You are not logged in", "error")
        return redirect(url_for('auth.login'))


@therapist_bp.route('/list')
def therapist_list():
    return render_template('therapist/therapist_list.html', active_page='therapist_list')

@therapist_bp.route('/card')
def therapist_card():
    return render_template('therapist/therapist_card.html')

@therapist_bp.route('/profile')
def therapist_profiles():
    return render_template('therapist/therapist_profile.html',active_page='therapist_profiles')

@therapist_bp.route('/add')
def add_therapist():
    return render_template('therapist/add_therapist.html')

@therapist_bp.route('/edit')
def edit_therapist():
    return render_template('therapist/edit_therapist.html',active_page = 'edit_therapist')

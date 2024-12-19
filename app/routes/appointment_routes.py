from flask import Blueprint, render_template

appointment_bp = Blueprint('appointment', __name__)

@appointment_bp.route('/list')
def appoint_list():
    return render_template('appoint_list.html')

@appointment_bp.route('/')
def appoint():
    return render_template('appoint.html')

@appointment_bp.route('/book')
def book_appoint():
    return render_template('book_appoint.html')

@appointment_bp.route('/edit')
def edit_appoint():
    return render_template('edit_appoint.html')

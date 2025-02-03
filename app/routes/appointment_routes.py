from flask import Blueprint, render_template

appointment_bp = Blueprint('appointment', __name__)

@appointment_bp.route('/list')
def appoint_list():
    return render_template('appointment/appoint_list.html', active_page='therapy_plan')

@appointment_bp.route('/')
def appoint():
    return render_template('appointment/appoint.html',active_page='therapy_session')

@appointment_bp.route('/book')
def book_appoint():
    return render_template('appointment/book_appoint.html')

@appointment_bp.route('/edit')
def edit_appoint():
    return render_template('appointment/edit_appoint.html')

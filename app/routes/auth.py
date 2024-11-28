# app/routes/auth.py

from flask import Blueprint, request, flash, redirect, url_for, render_template
from flask_login import login_required, current_user
from app.services.auth_service import register_user, login_user_service, logout_user_service

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            data = {
                "username": request.form['username'],
                "email": request.form['email'],
                "password": request.form['password']
            }
            response = register_user(data)
            flash(response["message"], 'success')
            return redirect(url_for('auth.login'))
        except ValueError as e:
            flash(str(e), 'danger')
            return redirect(url_for('auth.register'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            data = {
                "email": request.form['email'],
                "password": request.form['password']
            }
            response = login_user_service(data)
            flash(response["message"], 'success')
            return redirect(url_for('main.welcome'))
        except ValueError as e:
            flash(str(e), 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    try:
        response = logout_user_service(current_user)
        flash(response["message"], 'success')
        return redirect(url_for('auth.login'))
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('main.welcome'))

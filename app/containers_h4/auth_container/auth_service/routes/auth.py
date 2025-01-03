import requests
from sqlalchemy import create_engine, text
import os  # Asegúrate de importar 'os' para las variables de entorno
from flask import Blueprint, request, jsonify, render_template_string
from flask_login import login_required, current_user
from sqlalchemy.orm import sessionmaker
from auth_service.services.auth_service import (
    register_user,
    login_user_service,
    logout_user_service,
)

# Definir la URL del servicio de base de datos y el servicio de plantillas
DB_SERVICE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@db_service:5432/artigow_db')
engine = create_engine(DB_SERVICE_URL)
SessionLocal = sessionmaker(bind=engine)
TEMPLATES_SERVICE_URL = 'http://templates_service:5006/templates'  # URL del servicio de plantillas

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
            return redirect(url_for('auth.login'))
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    # En vez de renderizar un template desde el sistema de archivos, hacemos una solicitud
    try:
        # Hacer la solicitud HTTP para obtener la plantilla de registro
        response = requests.get(f'{TEMPLATES_SERVICE_URL}/register.html')
        if response.status_code == 200:
            template_content = response.text
            return render_template_string(template_content)  # Usamos render_template_string para renderizar la plantilla HTML
        else:
            return jsonify({"error": "Template not found"}), 404
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"No se pudo conectar con el servicio de plantillas: {str(e)}"}), 500

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            data = {
                "email": request.form['email'],
                "password": request.form['password']
            }
            response = login_user_service(data)
            # Devuelve un mensaje en formato JSON en lugar de flash y redirigir
            return jsonify({"message": response["message"]}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    # En vez de renderizar un template desde el sistema de archivos, hacemos una solicitud
    try:
        # Hacer la solicitud HTTP para obtener la plantilla de login
        response = requests.get(f'{TEMPLATES_SERVICE_URL}/login.html')
        if response.status_code == 200:
            template_content = response.text
            return render_template_string(template_content)  # Usamos render_template_string para renderizar la plantilla HTML
        else:
            return jsonify({"error": "Template not found"}), 404
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"No se pudo conectar con el servicio de plantillas: {str(e)}"}), 500

@auth_bp.route('/logout')
@login_required
def logout():
    try:
        response = logout_user_service(current_user)
        # Devuelve un mensaje en formato JSON en lugar de flash y redirigir
        return jsonify({"message": response["message"]}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

engine = create_engine(DB_SERVICE_URL)

@auth_bp.route('/check_user/<int:user_id>', methods=['GET'])
def check_user(user_id):
    try:
        with engine.connect() as conn:
            result = conn.execute(text('SELECT * FROM users WHERE id = :user_id'), {'user_id': user_id})
            user = result.fetchone()
            if user:
                return jsonify(dict(user)), 200
            else:
                return jsonify({"error": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"No se pudo conectar con la base de datos: {str(e)}"}), 500
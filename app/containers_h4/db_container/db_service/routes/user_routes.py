from flask import Blueprint, request, jsonify
from db_service.models.userprof import UserProf
from db_service import db
import logging



user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users', methods=['POST'])
def register_user():
    data = request.get_json()

    # Verificar que los campos necesarios estén presentes
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Campos requeridos faltantes"}), 400

    new_user = UserProf(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Usuario registrado correctamente."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al registrar el usuario: {str(e)}"}), 500

@user_routes.route('/users/email/<email>', methods=['GET'])
def get_user_by_email(email):
    user = UserProf.query.filter_by(email=email).first()

    if user:
        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            # No es una buena práctica devolver la contraseña, aunque sea cifrada
        }), 200
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

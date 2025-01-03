from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from db_service.models.userprof import db  # Aquí se importan los modelos de la DB
from db_service.routes.user_routes import user_routes  # Importación de rutas
from config import Config

app = Flask(__name__)

# Cargar la configuración desde el archivo de configuración
app.config.from_object(Config)

# Asegúrate de que la URL de la base de datos esté configurada correctamente
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db_service:5432/artigow_db'

# Registrar el blueprint para las rutas
app.register_blueprint(user_routes)

# Inicializar la base de datos con la aplicación Flask
db.init_app(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route('/')
def health_check():
    return "DB Service is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5433)


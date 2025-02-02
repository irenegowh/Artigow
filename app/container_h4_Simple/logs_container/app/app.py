from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2 import sql
import os

app = Flask(__name__)

# Configuración de la base de datos
DATABASE_URL = os.getenv('DATABASE_URL')  # Render proporciona DATABASE_URL
if not DATABASE_URL:
    raise RuntimeError("La variable de entorno DATABASE_URL no está definida")

TABLE_NAME = 'application_logs'


def init_db():
    """Crea la tabla para los logs si no existe."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute(sql.SQL(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                level VARCHAR(10),
                module VARCHAR(50),
                message TEXT
            )
        """))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        raise


@app.route('/log', methods=['POST'])
def receive_log():
    """Recibe logs vía HTTP POST y los almacena en la base de datos."""
    data = request.json
    level = data.get('level')
    module = data.get('module')
    message = data.get('message')

    if not (level and module and message):
        return jsonify({"error": "Datos incompletos"}), 400

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute(sql.SQL(f"""
            INSERT INTO {TABLE_NAME} (level, module, message)
            VALUES (%s, %s, %s)
        """), (level, module, message))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"status": "Log almacenado"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/query', methods=['POST'])
def run_query():
    """Recibe una consulta SQL y la ejecuta sobre la base de datos."""
    data = request.json
    query = data.get('query')

    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/', methods=['GET'])
def consulta_form():
    """Sirve el formulario HTML para hacer consultas SQL."""
    return render_template('logs_service.html')


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5003)

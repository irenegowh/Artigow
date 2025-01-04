from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2 import sql
import os

app = Flask(__name__)

# Configuración de la base de datos
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@db_service:5432/artigow_logs_db')
TABLE_NAME = 'application_logs'


def init_db():
    """Crea la tabla para los logs si no existe."""
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


@app.route('/log', methods=['POST'])
def receive_log():
    """Recibe logs vía HTTP POST y los almacena en la base de datos."""
    data = request.json
    level = data.get('level')
    module = data.get('module')
    message = data.get('message')

    # Validar datos recibidos
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
        
        # Ejecutar la consulta
        cursor.execute(query)

        # Obtener los resultados
        rows = cursor.fetchall()

        # Obtener los nombres de las columnas
        columns = [desc[0] for desc in cursor.description]

        # Convertir las filas en un diccionario con las columnas como claves
        result = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        conn.close()

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/', methods=['GET'])
def consulta_form():
    """Sirve el formulario HTML para hacer consultas SQL."""
    return render_template('logs_service.html')  # Asegúrate de que el archivo HTML está en la carpeta 'templates'

if __name__ == '__main__':
    init_db()  # Crear la tabla al iniciar
    app.run(host='0.0.0.0', port=5003)

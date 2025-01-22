from app import create_app, db
import psycopg2

app = create_app()

# Ejecutar la creación de las tablas dentro del contexto de la app
with app.app_context():
    db.create_all()  # Crear las tablas si es necesario

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


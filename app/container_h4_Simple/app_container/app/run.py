from app import create_app, db
import psycopg2

app = create_app()

# Ejecutar la creación de las tablas dentro del contexto de la app
with app.app_context():
    db.create_all()  # Crear las tablas si es necesario

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

try:
    conn = psycopg2.connect(
        dbname="artigowdb_2lqj",
        user="user",
        password="2ydBw1MGaHyvqbXYUiIWcweUsh5257SB",
        host="dpg-cu8g8elsvqrc73baddcg-a.frankfurt-postgres.render.com",
        port=5432
    )
    print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")

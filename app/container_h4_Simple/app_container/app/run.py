from app import create_app, db
from app.models import UserProf
import os

app = create_app()

# Crear las tablas dentro del contexto de la app
with app.app_context():
    db.create_all()  # Crear las tablas si es necesario

# Ejecutar la app
if __name__ == '__main__':
    # Obtén el puerto desde la variable de entorno o usa 5000 por defecto
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
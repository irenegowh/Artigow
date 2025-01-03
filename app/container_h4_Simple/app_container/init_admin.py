from app.models import UserProf
from app import create_app, db
from werkzeug.security import generate_password_hash  # Este es el método que usaremos para generar la contraseña cifrada

# Crea la instancia de la aplicación
app = create_app()

def create_admin_user():
    # Asegúrate de que el código se ejecute dentro del contexto de la aplicación
    with app.app_context():
        # Verifica si el usuario admin ya existe
        admin_user = UserProf.query.filter_by(username='admin').first()
        if not admin_user:
            # Crea un nuevo usuario administrador
            admin_user = UserProf(
                username='admin',
                email='admin@example.com',
                role='admin'  # Establece el rol como administrador
            )
            
            # Usa el setter para establecer la contraseña cifrada
            admin_user.set_password('adminpassword')  # Se usa el método 'set_password' para cifrar la contraseña

            # Añade el nuevo usuario a la sesión de la base de datos y realiza el commit
            db.session.add(admin_user)
            try:
                db.session.commit()
                print("Usuario administrador creado exitosamente.")
            except Exception as e:
                db.session.rollback()  # Rollback en caso de error
                print(f"Error al crear el usuario administrador: {e}")
        else:
            print("El usuario administrador ya existe.")

if __name__ == "__main__":
    create_admin_user()

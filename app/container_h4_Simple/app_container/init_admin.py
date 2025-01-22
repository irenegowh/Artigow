from app import create_app, db
from app.models import UserProf

app = create_app()

def create_admin_user():
    with app.app_context():
        admin_user = UserProf.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = UserProf(
                username='admin',
                email='admin@example.com',
                role='admin'  # Establece el rol como administrador
            )
            admin_user.set_password('adminpassword')
            db.session.add(admin_user)
            try:
                db.session.commit()
                print("Usuario administrador creado exitosamente.")
            except Exception as e:
                db.session.rollback()
                print(f"Error al crear el usuario administrador: {e}")
        else:
            print("El usuario administrador ya existe.")

if __name__ == "__main__":
    create_admin_user()

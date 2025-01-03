# app/repositories/auth_repository.py

from app.models.userprof import UserProf as User
from app import db

class AuthRepository:
    @staticmethod
    def add_user(username, email, password):
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

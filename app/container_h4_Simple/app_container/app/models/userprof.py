from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db

class UserProf(UserMixin, db.Model):
    __tablename__ = 'userprof'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)
    role = db.Column(db.String(20), default="user")  # "user" o "admin"

    # Relación con la clase Vote (un usuario puede tener muchos votos)
    votes = db.relationship('Vote', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == "admin"

    def __repr__(self):
        return f'<UserProf {self.username}>'

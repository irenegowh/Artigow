# app/models/__init__.py
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from .posts import Post
from .votes import Vote
from .userprof import UserProf
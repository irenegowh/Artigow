# app/models/__init__.py
from flask import current_app
from app import db

from .posts import Post
from .votes import Vote
from .userprof import UserProf
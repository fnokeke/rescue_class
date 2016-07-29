# models.py

from flask_sqlalchemy import SQLAlchemy
from rescue_class import app


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), primary_key=True, unique=True)
    access_token = db.Column(db.String(1200), primary_key=True, unique=True)

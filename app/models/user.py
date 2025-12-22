from flask_login import UserMixin
from ..extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
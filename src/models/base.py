"""Module for base model"""
from .database import db


class BaseModel(db.Model):
    """Parent model for abstracting routine methods/properties"""
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

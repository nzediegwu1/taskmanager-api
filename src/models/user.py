"""Module for User model"""
from .base import BaseModel
from .database import db


class User(BaseModel):
    """Defines database columns in user table"""
    __tablename__ = 'users'

    email = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<User {self.name}'

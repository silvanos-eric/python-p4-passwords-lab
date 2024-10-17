from config import db
from mixins import PasswordMixin
from sqlalchemy_serializer import SerializerMixin


class User(db.Model, SerializerMixin, PasswordMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)

    def __repr__(self):
        """Return a string representation of the user."""
        return f'User {self.username}, ID: {self.id}'

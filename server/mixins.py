from config import bcrypt, db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin


class PasswordMixin:
    _password_hash = db.Column(db.String, nullable=False)

    @hybrid_property
    def password_hash(self):
        """Prevent direct access to the password hash."""
        raise AttributeError('Password hashes are private.')

    @password_hash.setter
    def password_hash(self, password):
        """Hash the password using bcrypt and stor it"""
        self._password_hash = bcrypt.generate_password_hash(password).decode(
            'utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash,
                                          password).encode('utf-8')

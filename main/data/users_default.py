import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class UsersDefault(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users_default'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)
    tag = sa.Column(sa.String, index=True, unique=True, nullable=True)
    email = sa.Column(sa.String, nullable=True, unique=True)
    hashed_password = sa.Column(sa.String, default=None)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return f'<User name="{self.name}" id={self.id}>'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

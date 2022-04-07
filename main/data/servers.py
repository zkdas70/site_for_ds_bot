import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

users_to_servers = orm.relation("users_to_servers",
                                secondary="users",
                                backref="server",)


class servers(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'servers'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)

    def __repr__(self):
        return f'<server name="{self.name}" id={self.id}>'
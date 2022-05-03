import sqlalchemy as sa
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class UsersToServers(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users_to_servers'
    autoincrement = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    server = sa.Column(sa.Integer, sa.ForeignKey('servers.id'), index=True)
    users = sa.Column(sa.Integer, sa.ForeignKey('users_default.id'), index=True)
    coins = sa.Column(sa.Float, nullable=False, default=0)
    roles = sa.Column(sa.JSON, nullable=False, default=set())
    is_admin = sa.Column(sa.Boolean, default=False, nullable=False)

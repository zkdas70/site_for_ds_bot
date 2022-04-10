import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class TaskToServers(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'task_to_servers'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    task = sa.Column(sa.Integer, sa.ForeignKey('tasks.id'))
    server = sa.Column(sa.Integer, sa.ForeignKey('servers.id'))


import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

task_to_servers = sa.Table(
    'task_to_servers',
    SqlAlchemyBase.metadata,
    sa.Column('task', sa.Integer, sa.ForeignKey('tasks.id')),
    sa.Column('server', sa.Integer, sa.ForeignKey('servers.id')),
)


class tasks(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'tasks'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)
    task = sa.Column(sa.String, nullable=True)
    ansver = sa.Column(sa.String, nullable=True)
    coins = sa.Column(sa.Float, default=0)  # надо изменить этот сток пожже
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return f'<User name="{self.name}" id={self.id}>'

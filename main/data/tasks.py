import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Tasks(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'tasks'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)
    task = sa.Column(sa.String, nullable=True)
    ansver = sa.Column(sa.String, nullable=True)
    coins = sa.Column(sa.Float, default=0)  # надо изменить этот сток пожже
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return f'<User name="{self.name}" id={self.id}>'

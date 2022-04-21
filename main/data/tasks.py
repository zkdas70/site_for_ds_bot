import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Tasks(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'tasks'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    task = sa.Column(sa.String, nullable=False)
    answer = sa.Column(sa.String, nullable=False)
    coins = sa.Column(sa.Float, default=0, nullable=False)  # надо изменить этот сток пожже
    is_private = sa.Column(sa.Boolean, default=True, nullable=False)
    creator = sa.Column(sa.Integer, nullable=False)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now(), nullable=False)

import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Ad(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'ad'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    phone_number = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    salary = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    categories = orm.relation("Category", secondary="association", backref="ad")

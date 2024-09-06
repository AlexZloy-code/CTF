import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Jobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    full_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    balls = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    creator = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    job = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    img = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    link = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.String,
                                sqlalchemy.ForeignKey("users.id"))
    flag = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = orm.relationship('User')

    def __repr__(self):
        return self.name
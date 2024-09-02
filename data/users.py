import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    jobs = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    job = orm.relationship("Jobs", back_populates='user')
    is_active = True
    is_authenticated = True
    
    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return self.name

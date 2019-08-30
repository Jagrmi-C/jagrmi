# from sqlalchemy import create_engine
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person_table'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50))
    lastname = sa.Column(sa.String(50))
    birthdate = sa.Column(sa.String(50))
    birthplace = sa.Column(sa.String(100))

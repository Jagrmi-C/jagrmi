from datetime import datetime

# from sqlalchemy import create_engine
import sqlalchemy as sa
from aiopg.sa import create_engine
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy_imageattach.entity import Image, image_attachment
from sqlalchemy.orm import relationship

from settings import DSN

Base = declarative_base()


class Person(Base):
    __tablename__ = 'person'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.String(50), nullable=False)
    last_name = sa.Column(sa.String(50), nullable=False)
    birth_date = sa.Column(sa.DateTime(), nullable=False)
    birth_country_id = sa.Column(sa.Integer, sa.ForeignKey('country.id'))
    birth_place = sa.Column(sa.String(20))
    died_date = sa.Column(sa.DateTime())
    died_country_id = sa.Column(sa.Integer, sa.ForeignKey('country.id'))
    died_place = sa.Column(sa.String(20))
    last_date_edition = sa.Column(sa.DateTime(), default=datetime.utcnow)

# class PersonEntity(Base):
#     __tablename__ = 'person_entity_table'

#     id = sa.Column(sa.Integer, primary_key=True)
#     name = sa.Column(sa.String(50))
#     lastname = sa.Column(sa.String(50))
#     birthdate = sa.Column(sa.String(50))
#     birthplace = sa.Column(sa.String(100))
#     picture = image_attachment('PersonEntityPicture')

# class PersonEntityPicture(Base, Image):
#     __tablename__ = 'user_picture'

#     user_id = sa.Column(sa.Integer, sa.ForeignKey('person_entity.id'), primary_key=True)
#     user = relationship('PersonEntity')


class UserGoogle(Base):
    __tablename__ = 'user_google'

    google_id = sa.Column(sa.String(50), primary_key=True)
    google_user = sa.Column(sa.String(50))
    google_email = sa.Column(sa.String(50))

    def __init__(self, google_id, google_user, google_email):
        self.google_id = google_id
        self.google_user = google_user
        self.google_email = google_email

    def __repr__(self):
        return '<UserGoogle: {} {}>'.format(self.google_id, self.google_user)


class Country(Base):
    __tablename__ = "country"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(50), nullable=False)
    is_exist = sa.Column(sa.Boolean())
    person = relationship("Person")

    def __init__(self, country_id, name, is_active):
        self.country_id = country_id
        self.name = name
        self.is_active = is_active

    def __repr__(self):
        return '<Country: {} {}>'.format(self.is_active, self.name)


async def setup(app):
    engine = await create_engine(DSN)
    engine.Base = Base
    app.db = engine


async def close(app):
    app.db.close()
    await app.db.wait_closed()
    app.db = None

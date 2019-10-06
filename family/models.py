# from sqlalchemy import create_engine
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy_imageattach.entity import Image, image_attachment
# from sqlalchemy.orm import relationship

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person_table'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50))
    lastname = sa.Column(sa.String(50))
    is_active = sa.Column(sa.Boolean())

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
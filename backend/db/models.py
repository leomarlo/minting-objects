from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Ensure this is hashed!
    # comments = relationship('Comment', back_populates='user')

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    # user_id = Column(Integer, ForeignKey('users.id'))
    # user = relationship('User', back_populates='comments')

    # Foreign keys for each entity
    # publication_id = Column(Integer, ForeignKey('publications.id'))
    # artwork_id = Column(Integer, ForeignKey('artworks.id'))
    # exhibition_id = Column(Integer, ForeignKey('exhibitions.id'))
    # blogpost_id = Column(Integer, ForeignKey('blogposts.id'))

class Publication(Base):
    __tablename__ = 'publications'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    authors = Column(String)
    journal = Column(String)
    year = Column(Integer)
    # comments = relationship('Comment', back_populates='publication')

class Artwork(Base):
    __tablename__ = 'artworks'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    medium = Column(String)
    year = Column(Integer)
    # comments = relationship('Comment', back_populates='artwork')

class Exhibition(Base):
    __tablename__ = 'exhibitions'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    location = Column(String)
    year = Column(Integer)
    # comments = relationship('Comment', back_populates='exhibition')

class BlogPost(Base):
    __tablename__ = 'blogposts'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text)
    link = Column(String)  # If it's external
    date_posted = Column(DateTime, default=datetime.utcnow)
    # comments = relationship('Comment', back_populates='blogpost')

class CV(Base):
    __tablename__ = 'cv'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)



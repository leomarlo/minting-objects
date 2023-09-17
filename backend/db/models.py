from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
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


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    cid = Column(String, nullable=False)
    gs = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


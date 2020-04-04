import os
import json

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_user_id = Column(Integer, unique=True, nullable=False)
    telegram_chat_id = Column(Integer)
    test_col = Column(String(10))

class Content(Base):
    __tablename__ = 'contents'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    status = Column(String(10))


config = {}
with open(os.path.join('..', 'cfg', 'config.json')) as f:
    config = json.load(f)

from sqlalchemy import engine_from_config
engine = engine_from_config(config['database'])

from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
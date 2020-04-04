from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from db.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_user_id = Column(Integer, unique=True, nullable=False)
    telegram_chat_id = Column(Integer)

    contents = relationship('Content')

    def __init__(self, telegram_user_id):
        self.telegram_user_id = telegram_user_id

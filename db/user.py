from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_user_id = Column(Integer, unique=True, nullable=False)
    telegram_chat_id = Column(Integer)
    current_content_id = Column(Integer, ForeignKey('contents.id'), nullable=True)

    current_content = relationship('Content', foreign_keys=[current_content_id])
    contents = relationship('Content', primaryjoin='User.id == Content.user_id')

    def __init__(self, telegram_user_id):
        self.telegram_user_id = telegram_user_id

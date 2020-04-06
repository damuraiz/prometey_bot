from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base


class Content(Base):
    __tablename__ = 'contents'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    status = Column(String(10))
    user_id = Column('user_id', Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', foreign_keys=[user_id])
    videos = relationship('Video', primaryjoin='Content.id == Video.content_id')

    def __init__(self, name, status):
        self.name = name
        self.status = status

    def __repr__(self):
        return f"<Content(id='{self.id}', name='{self.name}', status='{self.status}')>"

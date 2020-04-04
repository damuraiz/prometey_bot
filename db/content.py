from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base


class Content(Base):
    __tablename__ = 'contents'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    status = Column(String(10))
    user_id = Column('user_id', Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User')

    def __init__(self, name, status):
        self.name = name
        self.status = status

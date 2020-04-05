from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base

class Video(Base):

    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True)
    url = Column(String(200), nullable=False)
    duration = Column(Integer)

    content_id = Column(Integer, ForeignKey('contents.id'), nullable=False)

    content = relationship('Content', foreign_keys=[content_id])

    def __init__(self, url):
        self.url = url

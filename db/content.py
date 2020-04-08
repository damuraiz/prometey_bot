from sqlalchemy import Column, Integer, String, ForeignKey, select, func, and_
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.ext.hybrid import hybrid_property

from db.base import Base

from db.video import Video


class Content(Base):
    __tablename__ = 'contents'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    status = Column(String(10))
    user_id = Column('user_id', Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', foreign_keys=[user_id])
    videos = relationship('Video', primaryjoin='Content.id == Video.content_id')

    total_video_count = column_property(
        select([func.count(Video.id)]).where(Video.content_id == id).correlate_except(Video)
    )

    total_duration = column_property(
        select([func.sum(Video.duration)]).where(Video.content_id == id).correlate_except(Video)
    )

    downloaded_video_count = column_property(
        select([func.count(Video.id)]).where(
            and_(
                Video.content_id == id,
                Video.status == 'DOWNLOADED'
            )
        ).correlate_except(Video)
    )

    @hybrid_property
    def all_downloaded(self):
        return self.total_video_count == self.downloaded_video_count

    def __init__(self, name, status):
        self.name = name
        self.status = status

    def __repr__(self):
        return f"<Content(id='{self.id}', name='{self.name}', status='{self.status}')>"

import os

from core.aws import PrometeyAmazon
from core.downloader import PrometeyDownloader
from db.user import User
from db.content import Content
from db.video import Video

from db.base import Session, engine, Base
from core.config import config

from urllib.parse import urlparse

from core.transactional import Transactional


class PrometeyService():
    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = Session()
        self.__downloader = PrometeyDownloader()
        self.__amazon = PrometeyAmazon(config['aws'])

    @Transactional
    def register_user(self, telegram_user_id):
        user = User(telegram_user_id)
        self.session.add(user)
        return user

    @Transactional
    def get_user(self, telegram_user_id):
        user = self.session.query(User).filter(User.telegram_user_id == telegram_user_id).one_or_none()
        return user

    @Transactional
    def create_content(self, user_id, name):
        content = Content(name, 'DRAFT')
        content.user_id = user_id
        self.session.add(content)
        self.session.flush()
        user = self.session.query(User).filter(User.id == user_id).one()
        user.current_content = content
        return content

    @Transactional
    def change_current(self, user_id, new_content_id):
        user = self.session.query(User).filter(User.id == user_id).one()
        user.current_content_id = new_content_id

    @Transactional
    def add_url(self, user_id, url):
        user = self.session.query(User).filter(User.id == user_id).one()
        t = urlparse(url)
        if user.current_content and user.current_content.status == 'DRAFT' and t.hostname == 'vm.tiktok.com':
            video = Video(url)
            user.current_content.videos.append(video)
            return video
        else:
            pass  # todo ошибка

    @Transactional
    def finish_video(self, user_id):
        user = self.session.query(User).filter(User.id == user_id).one()
        content = user.current_content
        if content:
            content.status = 'FINISHED'
            user.current_content_id = None
            return content

    # stay
    def get_download_list(self):
        videos = self.session.query(Video).join(Content). \
            filter(Video.status == 'NEW').limit(3)
        return videos

    @Transactional
    def set_video_status_downloaded(self, video):
        video.status = 'DOWNLOADED'

    @Transactional
    def get_content_to_encode(self):
        content = self.session.query(Content).join(Video). \
            filter(Content.status == "FINISHED"). \
            filter(Content.all_downloaded).first()
        return content

    @Transactional
    def get_content_to_send(self):
        content = self.session.query(Content).filter(Content.status == "READY").first()
        return content

    @Transactional
    def set_content_status(self, content, status):
        content.status = status
        return content

    def download_videos(self):
        videos = self.get_download_list()
        for video in videos:
            self.__download_video(video)
        return videos

    @Transactional
    def __download_video(self, video):
        data = self.__downloader.download_video(video.url)
        print(f'{video.url} - скачано из сети.')
        key = f'{video.content_id}/{video.id}.mp4'
        print(f'Загружаю на s3 {key}')
        print(self.__amazon.upload(key, data))
        video.status = 'DOWNLOADED'


if __name__ == '__main__':
    service = PrometeyService()
    print('-' * 100)
    service.download_videos()

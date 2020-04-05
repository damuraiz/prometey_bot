from db.user import User
from db.content import Content
from db.video import Video

from db.base import Session, engine, Base

from core.transactional import Transactional

class PrometeyService():
    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = Session()

    @Transactional
    def register_user(self, telegram_user_id):
        user = User(telegram_user_id)
        self.session.add(user)

    def create_content(self, user_id, name):
        content = Content(name, 'DRAFT')
        content.user_id = user_id
        self.session.add(content)


    def change_video(self, user_id, chat_id, new_video_id):
        pass

    def add_url(self, user_id, url):
        pass

    def download_videos(self):
        pass

    def finish_video(self, user_id, chat_id, video_id):
        pass

    def prepare_video(self):
        pass

    def get_video_info(self, video_id):
        pass

    def get_ready_videos(self):
        pass

    def get_user_videos(self, user_id):
        pass

if __name__ == '__main__':
    service = PrometeyService()
    service.register_user(1111)
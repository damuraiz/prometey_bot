import os
import sys
import json

from service import PrometeyService
from core.downloader import PrometeyDownloader
from core.encoder import PrometeyEncoder

import logging

class PrometeyDaemon():

    def __init__(self):
        self.__service = PrometeyService()
        self.__downloader = PrometeyDownloader()

        with open(os.path.join('cfg', 'config.json')) as f:
            config = json.load(f)
        self.temp_dir = config['temp_dir']
        self.__check_dir(self.temp_dir)

        self.__encoder = PrometeyEncoder(config['encoder'])

    def __check_dir(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    def __download_video(self, video):
        dir = os.path.join(self.temp_dir, str(video.content_id))
        name = str(video.id) + '.mp4'
        self.__check_dir(dir)
        self.__downloader.save_video(video.url, dir, name)
        video.duration = int(self.__encoder.get_duration(os.path.join(dir, name)))
        self.__service.set_video_status_downloaded(video)

    def download(self):
        download_list = self.__service.get_download_list()
        for video in download_list:
            logging.info(f'Скачиваю {video.url}')
            self.__download_video(video)


    def prepare(self):
        content = self.__service.get_content_to_encode()
        if content:
            logging.info(f'Начинаю собирать контент {content.id}:{content.name}')
            content = self.__service.set_content_status(content, 'PROCESSING')
            directory = os.path.join(self.temp_dir, str(content.id))
            portrait_name = directory + content.name + '-portrait.mp4'
            landscape_name = directory + content.name + '-landscape.mp4'
            files = [os.path.join(directory, f) for f in sorted(os.listdir(directory))
                     if os.path.isfile(os.path.join(directory, f)) and f.find(".mp4") != -1]
            print(portrait_name)
            print(landscape_name)
            print(files)
            self.__encoder.concat_clips(files, portrait_name)
            self.__encoder.landscape_video(portrait_name, landscape_name)
            logging.info(f'Контент собран {content.id}:{content.name}')
            self.__service.set_content_status(content, 'READY')


if __name__ == '__main__':
    args = sys.argv[1]
    daemon = PrometeyDaemon()

    if 'd' in args:
        daemon.download()
    if 'p' in args:
        daemon.prepare()
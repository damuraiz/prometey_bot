import os
import sys
import json

from service import PrometeyService
from core.downloader import PrometeyDownloader

class PrometeyDaemon():

    def __init__(self):
        self.__service = PrometeyService()
        self.__downloader = PrometeyDownloader()

        with open(os.path.join('cfg', 'config.json')) as f:
            config = json.load(f)
        self.temp_dir = config['temp_dir']
        self.__check_dir(self.temp_dir)

    def __check_dir(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    def __download_video(self, video):
        dir = os.path.join(self.temp_dir, str(video.content_id))
        self.__check_dir(dir)
        self.__downloader.save_video(video.url, dir, str(video.id) + '.mp4')
        self.__service.set_video_status_downloaded(video)

    def download(self):
        download_list = self.__service.get_download_list()
        for video in download_list:
            self.__download_video(video)

    def prepare(self):
        pass

if __name__ == '__main__':
    args = sys.argv[1]
    daemon = PrometeyDaemon()

    if 'd' in args:
        daemon.download()
        print("download")
    if 'p' in args:
        daemon.prepare()
        print('prepare')
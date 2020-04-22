import os
import sys
import json
import boto3
import paramiko
import time


from service import PrometeyService
from core.downloader import PrometeyDownloader
from core.encoder import PrometeyEncoder


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
            print(f'Скачиваю {video.url}')
            self.__download_video(video)


    def prepare(self):
        content = self.__service.get_content_to_encode()
        if content:
            print(f'Начинаю собирать контент {content.id}:{content.name}')
            #content = self.__service.set_content_status(content, 'PROCESSING')
            instance_id = "i-065f4b4ffb3b42d3c"
            ec2 = boto3.resource('ec2')
            instance = ec2.Instance(self.__encoder.config['instance_id'])

            key = paramiko.RSAKey.from_private_key_file(self.__encoder.config['instance_access_key_path'])
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            print('Стартую инстанс')
            instance.start()
            instance.wait_until_running()
            time.sleep(5)
            print('Инстанс стартовал')

            command = f'cd prometey_bot && s3fs prometey temp && python3 preparer.py  >> temp/last.log'
            try:
                client.connect(hostname=instance.public_ip_address, username='ubuntu', pkey=key)
                print('Запускую скрипт')
                client.exec_command(command)
                print('Скрипт отработал')
                client.close()
            except Exception as e:
                print(e)

            print('Жду дополнительные 60 секунд')
            time.sleep(60)
            print('Останавливаю инстанс')
            instance.stop()
            instance.wait_until_stopped()
            print('Инстанс остановлен')

            #self.__service.set_content_status(content, 'READY')


if __name__ == '__main__':
    args = sys.argv[1]
    daemon = PrometeyDaemon()

    if 'd' in args:
        daemon.download()
    if 'p' in args:
        daemon.prepare()
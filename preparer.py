#Этот скрипт будет собирать общий видео файл на отдельном инстансе aws
import json
import os
import sys
import time

import boto3

from core.config import config

from core.encoder import PrometeyEncoder
from core.aws import PrometeyAmazon


class ContentPreparer():

    def __init__(self, config, content_id, content_name):
        self.__encoder = PrometeyEncoder(config['encoder'])
        self.__amazon = PrometeyAmazon(config['aws'])
        self.__content_id = content_id
        self.__content_name = content_name
        self.__temp_dir = config['temp_dir']

    def test(self):
        s3 = boto3.resource("s3",
                            aws_access_key_id='AKIAXDNR6R3OJOF4M6CH',
                            aws_secret_access_key='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')
        bucket = s3.Bucket("prometey")
        dir = os.path.join(self.__temp_dir, str(self.__content_id))
        if not os.path.exists(dir):
            os.makedirs(dir)
        for obj in bucket.objects.filter(Prefix=f'{20}/'):
            print(obj.key)
        # os.mkdir(os.path.join())
        # content_id = 25
        # for obj in bucket.objects.filter(Prefix=f'{content_id}/24'):
        #     print(obj.key)
        #     with open('test24.mp4', 'wb') as f:
        #         f.write(obj.get()['Body'].read())


    def run(self):
        print(f'Начинаю собирать контент {self.__content_id}:{self.__content_name}')
        directory = os.path.join(self.__temp_dir, str(self.__content_id))
        portrait_name = directory + self.__content_name + '-portrait.mp4'
        landscape_name = directory + self.__content_name + '-landscape.mp4'
        files = [os.path.join(directory, f) for f in sorted(os.listdir(directory))
                 if os.path.isfile(os.path.join(directory, f)) and f.find(".mp4") != -1]
        print(portrait_name)
        print(landscape_name)
        print(files)
        print('Занимаюсь склейкой')
        self.__encoder.concat_clips(files, portrait_name)
        print("Жду 60 сек")
        time.sleep(60)
        print('Финальная обработка')
        self.__encoder.landscape_video(portrait_name, landscape_name)
        print(f'Контент собран {self.__content_id}:{self.__content_name}')

    def run2(self):
        print(f'Начинаю собирать контент {self.__content_id}:{self.__content_name}')
        os.makedirs(str(self.__content_id), exist_ok=True)
        for name, body in self.__amazon.files(self.__content_id):
            path = os.path.join(str(self.__content_id), name)
            with open(path, 'wb') as f:
                f.write(body)
        





Usage = f'\n\t {sys.argv[0]} ContentId ContentName'
ExampleUsage = f'\n\t Example {sys.argv[0]} 10 yohoho \n'
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("\n\t Two(2) arguments expected, {0} given.".format(len(sys.argv)-1))
        print(ExampleUsage)
        sys.exit(1)
    else:
        pass #todo проверка на форматы.

    with open(os.path.join('cfg', 'config.json')) as f:
        config = json.load(f)

    preparer = ContentPreparer(config, int(sys.argv[1]), sys.argv[2])

    preparer.run2()



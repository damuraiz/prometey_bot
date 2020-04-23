#Этот скрипт будет собирать общий видео файл на отдельном инстансе aws
import json
import os
import sys
import shutil


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
        self.__directory = os.path.join(self.__temp_dir, str(self.__content_id))
        self.__name_portrait = self.__directory + self.__content_name + '-portrait.mp4'
        self.__name_landscape = self.__directory + self.__content_name + '-landscape.mp4'



    def run(self):
        self.__download_files()
        self.__compile_files()
        self.__upload_files()
        self.__clean_files()

    def __download_files(self):
        print(f'Начинаю собирать контент {self.__content_id}:{self.__content_name}')
        os.makedirs(os.path.join(self.__temp_dir, str(self.__content_id)), exist_ok=True)
        for name, body in self.__amazon.files(self.__content_id):
            path = os.path.join(self.__temp_dir, str(self.__content_id), name)
            with open(path, 'wb') as f:
                print(f"Скачиваю {name}")
                f.write(body)
        print(f'Файлы скачаны для {self.__content_id}:{self.__content_name}')


    def __compile_files(self):
        files = [os.path.join(self.__directory, f) for f in sorted(os.listdir(self.__directory))
                 if os.path.isfile(os.path.join(self.__directory, f)) and f.find(".mp4") != -1]
        print(files)
        print('Занимаюсь склейкой')
        self.__encoder.concat_clips(files, self.__name_portrait)
        print('Финальная обработка')
        self.__encoder.landscape_video(self.__name_portrait, self.__name_landscape)
        print(f'Контент собран {self.__content_id}:{self.__content_name}')


    def __upload_files(self):
        print(f'Закидываю результат {self.__name_landscape} на s3')
        with open(self.__name_landscape, 'rb') as f:
            self.__amazon.upload(self.__name_landscape, f.read())
        print(f'Результат {self.__name_landscape} отправлен на s3')

    def __clean_files(self):
        print('Подчищаю временные файлы')
        os.remove(self.__name_portrait)
        os.remove(self.__name_landscape)
        shutil.rmtree(self.__directory)





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

    preparer.run()



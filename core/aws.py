import boto3
import os


class PrometeyAmazon():

    def __init__(self, config):
        self.__config = config
        id, key = config['aws_access_key_id'], config['aws_secret_access_key']
        self.__s3client = boto3.client('s3', aws_access_key_id=id, aws_secret_access_key=key)
        self.__s3 = boto3.resource('s3', aws_access_key_id=id, aws_secret_access_key=key)

    # todo нужна проверка реально прошла ли закачка.
    def upload(self, name, body):
        return self.__s3client.put_object(Bucket=self.__config['aws_bucket'],
                                          Body=body,
                                          Key=name)

    def files(self, content_id):
        bucket = self.__s3.Bucket(self.__config['aws_bucket'])
        for obj in bucket.objects.filter(Prefix=f"{content_id}/"):
            path, name = os.path.split(obj.key)
            yield name, obj.get()['Body'].read()

    def file(self, file):
        bucket = self.__s3.Bucket(self.__config['aws_bucket'])
        objects = bucket.objects.filter(Prefix=file)
        return objects[0].get()['Body'].read()


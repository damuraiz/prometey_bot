import time
import boto3
import datetime
import paramiko


before = datetime.datetime.now()

instance_id = "i-065f4b4ffb3b42d3c"
ec2 = boto3.resource('ec2')
instance = ec2.Instance(instance_id)

key = paramiko.RSAKey.from_private_key_file("../resources/prometey_compute.pem")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print('Стартую инстанс')
instance.start()
instance.wait_until_running()
time.sleep(5)
print('Инстанс стартовал')

command = 'cd prometey_bot && s3fs prometey temp && python3 daemon.py d >> temp/last.log'
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

after = datetime.datetime.now()
print(f"Elapsed time {after-before}")
#print(ec2.instances.all())
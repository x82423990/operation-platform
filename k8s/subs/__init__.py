import pika
import datetime

# 创建连接
user_pwd = pika.PlainCredentials('xie', 'Fs9006')
connection = pika.BlockingConnection(
    pika.ConnectionParameters('192.168.102.180', credentials=user_pwd, virtual_host='/vhost/fan'))

# 创建一个频道
channel = connection.channel()

channel.queue_declare(queue="hello")

channel.basic_publish(exchange='', routing_key='hello', body=str(datetime.datetime.now()))

print("[生产者] send success")
connection.close()

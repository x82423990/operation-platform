# import pika
#
#
# # 创建连接
# class Producer:
#     def __init__(self):
#         self.user_pwd = pika.PlainCredentials('xie', 'Fs9006')
#         self.connection = pika.BlockingConnection(
#             pika.ConnectionParameters('192.168.102.180', credentials=self.user_pwd, virtual_host='/vhost/fan'))
#
#     def pub(self, body):
#         # 创建一个频道
#         channel = self.connection.channel()
#         channel.queue_declare(queue="hello")
#         channel.basic_publish(exchange='', routing_key='hello', body=body)
#
#     def close(self):
#         self.connection.close()
#
#
# if __name__ == '__main__':
#     p = Producer()
#     p.pub("我是一个人")

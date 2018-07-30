# # import pika
#
# user_pwd = pika.PlainCredentials('xie', 'Fs9006')
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters('192.168.102.180', credentials=user_pwd, virtual_host='/vhost/fan'))
#
# # 创建一个频道
# channel = connection.channel()
#
# channel.queue_declare(queue="hello")
#
#
# def callback(ch, method, properties, body):
#     print(" [x] Received %r" % (body,))
#
#
# channel.basic_consume(callback, queue='hello', no_ack=False)
#
# print(' [*] Waiting for messages. To exit press CTRL+C')
# channel.start_consuming()

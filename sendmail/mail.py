from sendmail import Mail
content = "订阅消息"
s = Mail(content=content)
if s.send():
    print('success')
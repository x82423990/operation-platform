import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


class Mail:
    def __init__(self, content):
        self.content = content

    def _format_addr(self, s):
        name, add = parseaddr(s)
        return formataddr((name, add))

    def send(self, to=None, cc=None):
        from_add = "eatted@163.com"
        password = "xl50140872"
        to_add = to or ['xieyifan@hxbdtech.com', '82423990@qq.com']
        to_cc = cc or ['eatted@qq.com', ]
        smtp_server = "smtp.163.com"
        sub = "上线通知"
        body = self.content
        msg = MIMEMultipart()
        try:
            msg['From'] = self._format_addr('系统发布 <%s>' % from_add)
            msg['To'] = ','.join(to_add)
            msg['cc'] = ','.join(to_cc)
            msg['Subject'] = sub
            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP_SSL(host=smtp_server, port=465)
            # 如果使用SSL 则不用，反之亦然。
            # server.starttls()
            server.login(from_add, password=password)
            text = msg.as_string()
            server.sendmail(from_add, to_add, text)
            server.quit()
            return True
        except Exception as e:
            print(e)
            return False

if __name__ == '__main__':
    m = Mail(content='醍醐灌顶')
    m.send()

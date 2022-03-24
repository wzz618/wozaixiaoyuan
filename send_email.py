import smtplib
from email.mime.text import MIMEText
# email 用于构建邮件内容
from email.header import Header


class email_obj:
    def __init__(self, to_addr=None, email_Subject=None, email_content=None):
        data_inf_path = r'系统日志\email_data.txt'   # 邮箱信息的存储路径
        with open(data_inf_path, 'r+', encoding='UTF-8') as f:
            data_inf = eval(f.read())  # 读取邮箱信息
            f.close()
        self.from_addr = data_inf['发信邮箱']  # 发信邮箱
        self.password = data_inf['邮箱授权码']  # 发信邮箱的授权码
        self.smtp_server = data_inf['发信服务器']  # 发信服务器的域名
        self.to_addr = to_addr  # 收信邮箱
        self.email_Subject = email_Subject  # 邮件标题
        self.email_content = email_content  # 邮件内容

        # 开启发信服务，这里使用的是加密传输
        self.server = smtplib.SMTP_SSL(host=self.smtp_server)  # POP3/SMTP 协议的发送邮件服务器
        self.server.connect(self.smtp_server, 465)  # 使用SSL，端口号465
        # 登录发信邮箱
        self.server.login(self.from_addr, self.password)

    def change_email_inf_to(self, to_addr, email_Subject, email_content):
        self.to_addr = to_addr  # 收信邮箱
        self.email_Subject = email_Subject  # 邮件标题
        self.email_content = email_content  # 邮件内容

    def send(self):
        # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        msg = MIMEText(self.email_content, 'plain', 'utf-8')

        # 邮件头信息
        msg['From'] = Header(self.from_addr)
        msg['To'] = Header(self.to_addr)
        msg['Subject'] = Header(self.email_Subject)

        # 发送邮件
        self.server.sendmail(self.from_addr, self.to_addr, msg.as_string())

    def close(self):
        # 关闭服务器
        self.server.quit()


if __name__ == '__main__':
    to_addr = '3574403347@qq.com'
    email_Subject = 'send by python'
    email_content = 'python test'
    obj = email_obj(to_addr, email_Subject, email_content)
    obj.send()

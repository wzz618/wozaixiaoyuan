import socket
import json
import os
import time
import log_management
import data_store

# 建立一个服务端

# ip_port = ('localhost', 6998)
import traceback

import send_email

ip_port = ('0.0.0.0', 6998)
dataStr = {
    'no': 1,
    'name': 'Runoob',
    'url': 'http://www.runoob.com'
}
user_dir = 'user_data'


class Service:
    def __init__(self, log=None):
        if log is None:
            log = log_management.log_management()
        self.log = log

    def Start_service(self, port=6998):
        ip_port = ('0.0.0.0', int(port))
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ip_port)  # 绑定要监听的端口
        server.listen(5)  # 开始监听 表示可以使用五个链接排队
        self._print('服务器开始运行')
        while True:  # conn就是客户端链接过来而在服务端为期生成的一个链接实例
            conn, addr = server.accept()  # 等待链接,多个链接的时候就会出现问题,其实返回了两个值
            print(conn, addr)
            try:
                data = conn.recv(1024)  # 接收数据
                mesg = eval(data.decode())
                print('recive:', mesg)  # 打印接收到的数据
                if mesg['user_action'] == '提交':
                    # 保存信息
                    path = user_dir + '\\' + mesg['user_name'] + '.txt'
                    if not os.path.exists(os.path.dirname(path)):  # 如果文件目录不在，则创建目录
                        os.mkdir(os.path.dirname(path))
                    f = open(path, 'w+', encoding='UTF-8')
                    f.write(str(mesg))
                    f.close()
                    sendmesg = '提交成功'
                    # 邮箱提醒
                    admin_email = send_email.email_obj()  # 登录邮箱
                    email_Subject = '{}信息提交成功'.format(mesg['user_name'])
                    email_content = '用户{}，你选择的服务为晨检{}，午检{}，晚签到{}'.\
                        format(mesg['user_name'], mesg['晨检'], mesg['午检'], mesg['签到'])
                    admin_email.change_email_inf_to(to_addr=mesg['user_email'],
                                                    email_Subject=email_Subject,
                                                    email_content=email_content)
                    admin_email.send()
                    admin_email.close()
                elif mesg['user_action'] == '检查服务的时间':
                    path = '系统日志\\auto_time.txt'
                    f = open(path, 'r+', encoding='UTF-8')
                    auto_time = eval(f.read())
                    sendmesg = str(auto_time)
                else:
                    sendmesg = '请求错误'
                sendmesg = json.dumps(sendmesg)
                # conn.send(data.upper()) #然后再发送数据
                sendmesg = sendmesg.encode('utf-8')
                conn.send(sendmesg)
            except ConnectionResetError as e:
                print('关闭了正在占线的链接！')
                break

            conn.close()

    def _print(self, inf):
        if self.log is not None:
            self.log.write_data(inf)
            print(str(time.strftime("%H:%M:%S")) + '\t' + inf)
        else:
            print(str(time.strftime("%H:%M:%S")) + '\t' + inf)


if __name__ == '__main__':
    port = input('输入端口号')
    print('{}服务端系统开始运行'.format(data_store.academy[port]))
    while True:
        try:
            while True:
                aa = Service()
                aa.Start_service(port)
        except Exception:
            admin_email = send_email.email_obj()  # 登录邮箱
            email_Subject = '服务端错误退出'
            email_content = traceback.print_exc()
            qq_email = '3574403347@qq.com'
            admin_email.change_email_inf_to(to_addr=qq_email, email_Subject=email_Subject,
                                            email_content=email_content)
            admin_email.close()
            time.sleep(100)
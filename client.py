# -*- coding: UTF-8 -*-

import socket  # 客户端 发送一个数据，再接收一个数据
import time
import json

# ip_port = ('localhost', 6998)
ip_port = ('8.141.52.187', 6998)


class Client:
    def __init__(self, log=None):
        self.log = log
        self.client = None

    def send_inf(self, msg):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 声明socket类型，同时生成链接对象
        self.client.connect(ip_port)  # 建立一个链接，连接到本地的6969端口
        # addr = client.accept()
        # print '连接地址：', addr
        self._print(msg['user_action'])  # 输出我发送的信息
        msg = str(msg)
        self.client.send(msg.encode('utf-8'))  # 发送一条信息 python3 只接收btye流
        res = self.client.recv(1024)  # 接收一个信息，并指定接收的大小 为1024字节
        dataJson = json.loads(res.decode())
        # 如果返回的只是一个字符串，不是json数据，则替换成下面代码：
        # reciveStr = data.decode()
        self._print(dataJson)  # 输出我接收的信息
        self.client.close()  # 关闭这个链接
        return dataJson

    def _print(self, inf):
        if self.log is not None:
            self.log.write_data(inf)
            print(str(time.strftime("%H:%M:%S")) + '\t' + inf)
        else:
            print(str(time.strftime("%H:%M:%S")) + '\t' + inf)


if __name__ == '__main__':
    aa = Client()
    data = {
        'user_name': '请输入你的账号',
        'user_password': '请输入你的密码',
        'user_dormitory': '请输入你的宿舍号码',
        'user_email': '请输入你接受消息的邮箱',
        'user_action': '提交',
        'User-Agent': None,
        '晨检': 0,
        '午检': 0,
        '签到': 0
    }
    aa.send_inf(data)

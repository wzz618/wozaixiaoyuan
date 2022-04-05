import socket
import json
import os
import time

# 建立一个服务端

ip_port = ('localhost', 6998)
dataStr = {
    'no': 1,
    'name': 'Runoob',
    'url': 'http://www.runoob.com'
}
user_dir = 'user_data'


class Service:
    def __init__(self, log=None):
        self.log = log

    def Start_service(self):
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
                    f = open(path, 'w+')
                    f.write(str(mesg))
                    f.close()
                    sendmesg = '提交成功'
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
    aa = Service()
    aa.Start_service()
    # while True:
    #     try:
    #         aa = Service()
    #         aa.Start_service()
    #     except Exception as E:
    #         print(E)

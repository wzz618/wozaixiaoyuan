import os
import log_management
import time
import wozaixiaoyuan
import send_email
import traceback


class tip_email:
    def __init__(self):
        self.user_path = 'user_data\\'

        self.log = log_management.log_management()
        with open(r'系统日志\auto_time.txt', 'r+', encoding='UTF-8') as f:
            self.auto_time = eval(f.read())
        self._print('准备开始运行')
        self.run()

    def run(self):
        admin_email = send_email.email_obj()  # 登录邮箱
        for user_name in os.listdir(self.user_path):
            path = self.user_path + user_name
            with open(path, 'r', encoding='UTF-8') as f:
                user_data = eval(f.read())
                email_Subject = 'AUTO我在校园4.3.0版本2022.06.08正式运行内容提要'
                email_content = '1、本版本添加了自定义的user-agent选项，主要是为了伪装成对应的手机型号登录，防止可能存在的异常登录提示\n' \
                                '2、可以在本机微信打开这个网址https://www.ip138.com/useragent/。复制对应的user-agent信息即可（会包括arm64 Weixin ' \
                                'NetType）\n' \
                                '3、对应的电脑客户端可以在 https://github.com/wzz618/wozaixiaoyuan/tree/main/打包好的文件 处下载\n' \
                                '4、注意！！！推荐重新下载最新的客户端重新提交信息'
                admin_email.change_email_inf_to(to_addr=user_data['user_email'], email_Subject=email_Subject,
                                                email_content=email_content)
                admin_email.send()
        admin_email.close()

    def _print(self, inf):
        if self.log is not None:
            self.log.write_data(inf)
            print(str(time.strftime("%H:%M:%S")) + '\t' + inf)
        else:
            print(str(time.strftime("%H:%M:%S")) + '\t' + inf)


if __name__ == '__main__':
    aa = tip_email()
    aa.run()


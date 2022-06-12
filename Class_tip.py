import pandas as pd
import time
import send_email
import log_management
import wozaixiaoyuan
import os
import Class_tip_auto_tip

__version__ = '3.4.2'


class Class_tip:
    def __init__(self):
        # file_path
        self._main_path = os.path.dirname(os.path.abspath(__file__))
        self.log = log_management.log_management(doc_name='我在校园班级管理系统')

        # data
        self.admin_account = None  # dict 管理员的账号信息，用于登录我在校园
        self.class_manager = None  # dict 接受管理的账号信息
        self.classmate_data = None  # pandas frames 班级管理人员的信息
        self.tip_time = None  # dict 提醒的时间
        self.read_config()  # 读取上述的信息

        # auto_tip
        self.tip_type = None
        self.unfinished_classmate_names_list = []
        self._print('系统初始化完成')

    def read_config(self):
        """
            读取信息，丰富对象属性中的一些信息
        :return:
        """
        # 管理员的账号信息，用于登录我在校园
        with open(self._main_path + r'/系统日志/admin_account.txt', 'r+', encoding='UTF-8') as f:
            self.admin_account = eval(f.read())
        # 接受管理的账号信息
        with open(self._main_path + r'/系统日志/class_manager.txt', 'r+', encoding='UTF-8') as f:
            self.class_manager = eval(f.read())
        # 班级管理人员的信息
        self.classmate_data = pd.read_excel(self._main_path + r'/用户信息/班级成员信息.xlsx')
        # 提醒的时间
        with open(self._main_path + r'/系统日志/tip_time.txt', 'r+', encoding='UTF-8') as f:
            self.tip_time = eval(f.read())

    def _print(self, inf):
        """
        输出对应的数据信息
        :param inf: string 待输出的数据信息
        :return: None
        """
        if self.log is not None:
            self.log.write_data(inf)
            print(str(time.strftime("%Y-%m-%d %H:%M:%S")) + '\t' + inf)
        else:
            print(str(time.strftime("%Y-%m-%d %H:%M:%S")) + '\t' + inf)

    def auto_tip(self):
        while True:
            tip_type, time_loc, sleep_time = Class_tip_auto_tip.auto_tip_check(tip_time=self.tip_time)
            if tip_type is not None:
                # 进行提醒
                wzxy = wozaixiaoyuan.wozaixiaoyuan(log=self.log, ua=self.admin_account['User-Agent'])
                wzxy.login(self.admin_account['username'], self.admin_account['password'], )
                self.unfinished_classmate_names_list = Class_tip_auto_tip.get_unfinished_list(wzxy, tip_type)  # 需要提醒的人员列表
                admin_email = send_email.email_obj()  # 登录邮箱
                try:
                    # 一一提醒
                    if len(self.unfinished_classmate_names_list) != 0:
                        email_Subject = f'{tip_type}打卡提醒QAQ'
                        for name in self.unfinished_classmate_names_list:
                            qq = self.classmate_data.loc[self.classmate_data['姓名'] == name, 'QQ号'].values[0]
                            qq_email = str(qq) + '@qq.com'
                            email_content = f'成员{name}，您好\n现在北京时间{time.strftime("%H:%M:%S")}，' \
                                            f'而您尚未完成打卡，请及时完成{tip_type}打卡。\n（退订回复：0）\n注：本消息无法退订'
                            admin_email.change_email_inf_to(to_addr=qq_email, email_Subject=email_Subject,
                                                            email_content=email_content)
                            admin_email.send()
                            self._print(f'已经给成员{name}发送信息')
                    else:
                        pass
                    # 给管理员发送班级成员完成情况
                    if time_loc == len(self.tip_time[tip_type]) - 1:
                        for key in self.class_manager:  # 和管理员发消息
                            email_Subject = f'{tip_type}打卡消息提示'
                            qq_email = self.class_manager[key]['email']
                            email_content = f'管理员{key}，您好\n截止目前{time.strftime("%H:%M:%S")}，' \
                                            f'您的班级成员还有{self.unfinished_classmate_names_list}未完成打卡了\n。 '
                            admin_email.change_email_inf_to(to_addr=qq_email, email_Subject=email_Subject,
                                                            email_content=email_content)
                            admin_email.send()
                            self._print(f'已经给管理员{key}发送{tip_type}完成情况')

                            # 给管理员发送当前的日志
                            if tip_type == '签到':
                                email_Subject = f'{time.strftime("%Y-%m-%d")}日志消息'
                                email_content = self.log.today_data
                                admin_email.change_email_inf_to(to_addr=qq_email, email_Subject=email_Subject,
                                                                email_content=email_content)
                                admin_email.send()
                                self._print(f'已经给管理员{key}发送当天的日志消息')
                    admin_email.close()

                except Exception as e:
                    self._print(str(e))
                    time.sleep(2*60)
            self._print(f'即将睡眠{sleep_time}')
            time.sleep(seconds(sleep_time))


def seconds(now_time):  # 把时间转化为秒
    time_list = now_time.split(':')
    now_seconds = 0
    for i in range(len(time_list)):
        now_seconds += int(time_list[i]) * pow(60, 2-i)  # 换算成s
    return now_seconds


def to_StrTime(now_seconds):  # 把s转化为字符串
    m, s = divmod(now_seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)


if __name__ == '__main__':
    obj = Class_tip()
    obj.auto_tip()
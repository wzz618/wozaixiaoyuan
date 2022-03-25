import pandas as pd
import time
import send_email
import log_management
import wozaixiaoyuan

__version__ = '3.0'


class tip_system:
    def __init__(self, main_path):
        self._main_path = main_path
        self._tip_time_path = self._main_path + r'\系统日志\tip_time.txt'  # 提醒时间的存储位置
        self._admin = self._main_path + r'\系统日志\admin.txt'
        self._admin_path = self._main_path + r'\系统日志\admin_data.txt'  # 提醒时间的存储位置
        self._file_path = self._main_path + r'\用户信息\班级成员信息.xlsx'  # 班级成员的信息位置

        self.log = log_management.log_management(current_dir=self._main_path)  # 日志对象

        self.admin = None  # 管理员 list
        self.admin_data = None  # 管理员的账号信息
        self.file = None  # 人员姓名和qq号
        self.tip_time_inf = None  # 提醒事项和时间
        self.read_config()  # 上述三个的信息

        self._print('程序初始化完成')

        self.in_tips_time()
        self.Run()

    def read_config(self):  # 读取信息，丰富对象属性中的一些信息
        self.file = pd.read_excel(self._main_path + r'\用户信息\班级成员信息.xlsx')
        with open(self._tip_time_path, 'r+', encoding='UTF-8') as f:
            self.tip_time_inf = eval(f.read())
            f.close()
        with open(self._admin_path, 'r+', encoding='UTF-8') as f:
            self.admin = eval(f.read())
            f.close()
        with open(self._admin, 'r+', encoding='UTF-8') as f:
            self.admin_data = eval(f.read())
            f.close()
        self._print('信息读入完成')

    def in_tips_time(self):  # 判断是否在提醒时间
        # 获得现在的时间
        now_time_0 = time.strftime("%H:%M:%S")
        now_time = seconds(now_time_0)
        # 判断是否在提醒时间
        flag = 0  # 判断是否属于提醒时间
        ready_key = None  # 目前的提醒类型
        for key in self.tip_time_inf:
            for tips_time in self.tip_time_inf[key]:
                tips_time = seconds(tips_time)  # 提醒的时间
                if abs(now_time - tips_time) <= 60:  # 如果符合则退出
                    flag = 1
                    ready_key = key  # 获得当前的提醒类型
                    break
                else:
                    continue
            if flag == 1:
                break
        if flag == 0:
            self._print('当前时间是:{}，不在提醒时间'.format(now_time_0))
            return None
        else:
            self._print('当前时间是:{}，准备进行{}提醒'.format(now_time_0, ready_key))
            return ready_key

    def Run(self):
        try:
            while True:
                ready_key = self.in_tips_time()   # 获得当前的提醒类型
                if ready_key is not None:
                    # 进行提醒
                    wzxy = wozaixiaoyuan.wozaixiaoyuan(log=self.log)
                    wzxy.login(self.admin_data['username'], self.admin_data['password'])
                    name_list = self.tip(wzxy, ready_key)  # 需要提醒的人员列表
                    admin_email = send_email.email_obj()  # 登录邮箱
                    if name_list is None:  # 如果没有返回信息，说明已经完成了
                        email_Subject = '{}打卡提醒'.format(ready_key)
                        for key in self.admin:  # 和管理员发消息
                            qq_email = Get_email_address(self.file, [key])  # 管理员的qq邮箱
                            email_content = f'尊敬的2019340203班管理员{key}，您好\n截止目前{time.strftime("%H:%M:%S")}，' \
                                            f'您的班级成员已经全部完成{ready_key}打卡了\n。 '
                            admin_email.change_email_inf_to(to_addr=qq_email, email_Subject=email_Subject,
                                                            email_content=email_content)
                            admin_email.send()
                            self._print(f'已经给管理员{key}发送信息')
                    else:
                        # 给成员一一发送信息
                        email_Subject = '{}打卡提醒QAQ'.format(ready_key)
                        qq_email = Get_email_address(self.file, name_list)  # 成员的qq邮箱dict
                        for name in name_list:
                            email_content = f'尊敬的2019340203班成员{name}，您好\n现在北京时间{time.strftime("%H:%M:%S")}，' \
                                            f'而您尚未完成健康打卡，请及时完成{ready_key}打卡。\n（退订回复：0）\n注：本消息无法退订'
                            admin_email.change_email_inf_to(to_addr=qq_email[name], email_Subject=email_Subject,
                                                            email_content=email_content)
                            admin_email.send()
                            if name == self.admin_data['姓名']:  # 帮助打卡
                                self.help_do(wzxy, ready_key)
                                email_content = f'{name}的{ready_key}成功'
                                admin_email.change_email_inf_to(to_addr=qq_email[name], email_Subject=email_Subject,
                                                                email_content=email_content)
                                self._print(f'已经帮助管理员{name}打卡')
                        self._print(f'未打卡的人员为{name_list}')
                        # 给管理员发送信息
                        for key in self.admin:  # 和管理员发消息
                            qq_email = Get_email_address(self.file, [key])  # 管理员的qq邮箱
                            email_content = f'尊敬的2019340203班管理员{key}，您好\n截止目前{time.strftime("%H:%M:%S")}，' \
                                            f'您的班级成员已经全部完成{ready_key}打卡了\n。 '
                            admin_email.change_email_inf_to(to_addr=qq_email[key], email_Subject=email_Subject,
                                                            email_content=email_content)
                            admin_email.send()
                            self._print(f'已经给管理员{key}发送信息')
                time.sleep(self._sleep())
        except Exception as e:
            # 给管理员发送错误信息
            admin_email = send_email.email_obj()  # 登录邮箱
            email_Subject = '错误退出提醒'
            for key in self.admin:  # 和管理员发消息
                qq_email = Get_email_address(self.file, [key])  # 管理员的qq邮箱
                email_content = f'尊敬的2019340203班管理员{key}，您好\n截止目前{time.strftime("%H:%M:%S")}，' \
                                f'程序错误退出，退出错误类型为{e}\n。 '
                admin_email.change_email_inf_to(to_addr=qq_email, email_Subject=email_Subject,
                                                email_content=email_content)
                admin_email.send()
                self._print(email_content)
            admin_email.send()

    def tip(self, wzxy, inf):  # 获得提醒类型
        if inf == '晨检':
            return wzxy.get_HeatUsers(seq=1)
        elif inf == '午检':
            return wzxy.get_HeatUsers(seq=2)
        elif inf == '签到':
            return wzxy.get_SignResult()

    def help_do(self, wzxy, inf):  # 帮助管理员晨检
        if inf == '晨检':
            return wzxy.heat(seq=1)
        elif inf == '午检':
            return wzxy.heat(seq=2)

    def _sleep(self):
        now_time = time.strftime("%H:%M:%S")  # 获得当前的时间
        now_time_s = seconds(now_time)  # 转化为s
        to_time = 0  # 睡眠的时间
        sleep_time = 0  # 需要睡眠的时间
        # 排序需要提醒的时间列表
        tip_time_list = []
        for key in self.tip_time_inf:
            for time_inf in self.tip_time_inf[key]:
                tip_time_list.append(seconds(time_inf))  # 转化为s
        tip_time_list = sorted(tip_time_list)  # 排序

        if now_time_s > tip_time_list[-1]:
            # 如果超过当天的提醒时间
            sleep_time = 24 * 60 * 60 + tip_time_list[0] + now_time_s
            self._print('即将睡眠{}s，预计次日{}点苏醒'.format(sleep_time, to_StrTime(tip_time_list[0])))
        else:
            # 如果未超过当天的提醒时间
            for i in range(len(tip_time_list)):
                # 找到第一个大于当前时间的下一次提醒时间
                if tip_time_list[i] > now_time_s:
                    sleep_time = tip_time_list[i] - now_time_s
                    self._print('即将睡眠{}s，预计今日{}苏醒'.format(sleep_time, to_StrTime(tip_time_list[i])))
                    break
        return sleep_time

    def _print(self, inf):
        if self.log is not None:
            self.log.write_data(inf)
            print(str(time.strftime("%H:%M:%S")) + '\t' + inf)
        else:
            print(str(time.strftime("%H:%M:%S")) + '\t' + inf)


def Get_email_address(file, name_list):  # 获得文件中的qq邮箱
    address_dict = {}
    if len(name_list) == 0:
        pass
    elif len(name_list) == 1:
        qq = file.loc[file['姓名'] == name_list[0], 'QQ号'].values[0]
        qq_email = str(qq) + '@qq.com'
        return qq_email
    else:
        for i in range(len(name_list)):  # 依次编辑文件
            name_i = name_list[i]
            qq = file.loc[file['姓名'] == name_i, 'QQ号'].values[0]
            qq_email = str(qq) + '@qq.com'
            address_dict[name_i] = qq_email
        return address_dict


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
    tip_system(main_path=r'D:\小王的仓库\2号仓库（用于pycharm的存储）\我在校园自动提示2')


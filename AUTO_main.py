import os
import log_management
import time
import wozaixiaoyuan
import send_email
import traceback


class auto_main:
    def __init__(self):
        self.user_path = 'user_data\\'

        self.log = log_management.log_management()
        with open(r'系统日志\auto_time.txt', 'r+', encoding='UTF-8') as f:
            self.auto_time = eval(f.read())
        self._print('准备开始运行')
        self.run()

    def run(self):
        while True:
            with open(r'系统日志\auto_time.txt', 'r+', encoding='UTF-8') as f:
                self.auto_time = eval(f.read())
            ready_key = self._in_tips_time()
            if ready_key is not None:
                admin_email = send_email.email_obj()  # 登录邮箱
                for user_name in os.listdir(self.user_path):
                    path = self.user_path + user_name
                    with open(path, 'r', encoding='UTF-8') as f:
                        user_data = eval(f.read())
                    if user_data[ready_key] == 1:
                        try:
                            wzxy = wozaixiaoyuan.wozaixiaoyuan()
                            res = wzxy.login(user_data['user_name'], user_data['user_password'])
                            if res['code'] == 0:
                                email_Subject = '{}完成'.format(ready_key)
                                res = self.help_do(wzxy, ready_key)
                                email_content = '用户{}，你的打卡完成了，返回信息为{}'.format(user_data['user_name'], res)
                            else:
                                email_Subject = '密码修改提醒！！！'.format(ready_key)
                                email_content = '用户{}，您的密码{}已经失效，请及时在我在校园小程序更改密码'.format(user_data['user_name'], user_data['user_password'])
                            self._print(email_content)
                            admin_email.change_email_inf_to(to_addr=user_data['user_email'], email_Subject=email_Subject,
                                                            email_content=email_content)
                            admin_email.send()
                        except Exception as E:
                            self._print(E)
                    else:
                        pass
            # 进入睡眠
            time.sleep(self._sleep())
            self._print('苏醒')

    def _print(self, inf):
        if self.log is not None:
            self.log.write_data(inf)
            print(str(time.strftime("%H:%M:%S")) + '\t' + inf)
        else:
            print(str(time.strftime("%H:%M:%S")) + '\t' + inf)

    def _in_tips_time(self):
        now_time_0 = time.strftime("%H:%M:%S")
        now_time = seconds(now_time_0)
        # 判断是否在提醒时间
        flag = 0  # 判断是否属于提醒时间
        ready_key = None  # 目前的提醒类型
        for key in self.auto_time:
            tips_time = seconds(self.auto_time[key])  # 提醒的时间
            if abs(now_time - tips_time) <= 60:  # 如果符合则退出
                flag = 1
                ready_key = key  # 获得当前的提醒类型
                break
            else:
                pass
        if flag == 0:
            self._print('当前时间是:{}，不在打卡时间'.format(now_time_0))
            return None
        else:
            self._print('当前时间是:{}，准备进行{}打卡'.format(now_time_0, ready_key))
            return ready_key

    def _sleep(self):
        now_time = time.strftime("%H:%M:%S")  # 获得当前的时间
        now_time_s = seconds(now_time)  # 转化为s
        sleep_time = 0  # 需要睡眠的时间
        # 排序需要提醒的时间列表
        tip_time_list = []
        for key in self.auto_time:
            tip_time_list.append(seconds(self.auto_time[key]))
        tip_time_list = sorted(tip_time_list)  # 排序
        if now_time_s > tip_time_list[-1]:
            # 如果超过当天的提醒时间
            sleep_time = 24 * 60 * 60 + tip_time_list[0] - now_time_s
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

    def help_do(self, wzxy, inf):  # 帮助管理员晨检
        if inf == '晨检':
            return wzxy.heat(seq=1)
        elif inf == '午检':
            return wzxy.heat(seq=2)
        elif inf == '签到':
            return wzxy.sign()


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
    try:
        while True:
            auto_main()
    except Exception:
        admin_email = send_email.email_obj()  # 登录邮箱
        email_Subject = '自动打卡程序错误退出提醒'
        email_content = traceback.print_exc()
        qq_email = '3574403347@qq.com'
        admin_email.change_email_inf_to(to_addr=qq_email, email_Subject=email_Subject,
                                        email_content=email_content)

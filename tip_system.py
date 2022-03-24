import pandas as pd
import time
import send_email
import log_management

__version__ = '3.0'


class tip_system:
    def __init__(self, main_path):
        self._main_path = main_path
        self._tip_time_path = self._main_path + r'\系统日志\tip_time.txt'  # 提醒时间的存储位置
        self._admin_path = self._main_path + r'\系统日志\admin_data.txt'  # 提醒时间的存储位置
        self._file_path = self._main_path + r'\用户信息\班级成员信息.xlsx'  # 班级成员的信息位置

        self.log = log_management.log_management(current_dir=self._main_path)  # 日志对象

        self.admin = None  # 管理员 list
        self.file = None  # 人员姓名和qq号
        self.tip_time_inf = None  # 提醒事项和时间
        self.read_config()  # 上述三个的信息

        self.log.write_data('程序初始化完成')

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
        self.log.write_data('信息读入完成')

    def in_tips_time(self):  # 判断是否在提醒时间
        # 获得现在的时间
        now_time_0 = time.strftime("%H:%M:%S")
        now_time = seconds(now_time_0)
        # 判断是否在提醒时间
        flag = 0
        ready_key = None
        for key in self.tip_time_inf:
            for tips_time in self.tip_time_inf[key]:
                tips_time = seconds(tips_time)
                if abs(now_time - tips_time) <= 60:  # 如果符合则退出
                    flag = 1
                    ready_key = key  # 获得当前的提醒类型
                    break
                else:
                    continue
            if flag == 1:
                break
        if flag == 0:
            self.log.write_data('当前时间是:{}，不在提醒时间'.format(now_time_0))
            return None
        else:
            self.log.write_data('当前时间是:{}，准备进行{}提醒'.format(now_time_0, ready_key))
            return ready_key

    def Run(self):
        try:
            while True:
                if self.in_tips_time() is not None:
                    ready_key = self.in_tips_time()  # 获得当前的提醒类型
                    print('a')
        except Exception as e:
            admin_email = send_email.email_obj()  # 登录邮箱


def Get_email_address(file, name_list):  # 获得文件中的qq邮箱
    address_dict = {}
    if len(name_list) == 0:
        pass
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


if __name__ == '__main__':
    tip_system(main_path=r'D:\小王的仓库\2号仓库（用于pycharm的存储）\我在校园自动提示2')
    file = pd.read_excel(r'D:\小王的仓库\2号仓库（用于pycharm的存储）\我在校园自动提示2\用户信息\班级成员信息.xlsx')
    aa = Get_email_address(file, ['王政焯'])
    print(aa)


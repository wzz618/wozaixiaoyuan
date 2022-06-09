import wx
import os
import wozaixiaoyuan
import log_management
import client
import data_store


class frame(wx.Frame):
    def __init__(self):
        self.user_data_path = r'系统日志/user_data.txt'
        self.log = log_management.log_management()
        self.user_data = self.read_config()

        # 定义容器
        wx.Frame.__init__(self, None, -1, '我在校园自动签到系统', pos=(100, 100), size=(450, 500))
        self.Center()

        # 总容器
        sizer = wx.BoxSizer(wx.VERTICAL)

        # 输入界面
        sizer_input = wx.BoxSizer(wx.VERTICAL)
        sizer_user_name = wx.BoxSizer()
        sizer_user_password = wx.BoxSizer()
        sizer_user_email = wx.BoxSizer()
        sizer_User_Agent = wx.BoxSizer()
        sizer_user_dormitory = wx.BoxSizer()
        sizer_ip_port = wx.BoxSizer()
        sizer_tip_inf = wx.BoxSizer(wx.VERTICAL)
        # 捆绑按钮
        # sizer_user_name
        txt1 = wx.StaticText(self, -1, r'账号', style=wx.ST_NO_AUTORESIZE)  # 文字
        TextCtrl_user_name = wx.TextCtrl(self, value=self.user_data['user_name'], style=wx.TE_LEFT)  # 输入框
        self.Bind(wx.EVT_TEXT, lambda evt, textCtr='user_name': self.evt_txt(evt, textCtr), TextCtrl_user_name)  # 事件
        bt_user_help = wx.Button(self, label='账号帮助', size=(100, 25))

        sizer_user_name.Add(txt1, proportion=0, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        sizer_user_name.Add(TextCtrl_user_name, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)
        sizer_user_name.Add(bt_user_help, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        sizer_input.Add(sizer_user_name, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)

        # user_password
        txt2 = wx.StaticText(self, -1, r'密码', style=wx.ST_NO_AUTORESIZE)  # 文字
        TextCtrl_user_password = wx.TextCtrl(self, value=self.user_data['user_password'], style=wx.TE_LEFT)  # 输入框
        bt_pass_help = wx.Button(self, label='密码帮助', size=(100, 25))
        sizer_user_password.Add(txt2, proportion=0, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        sizer_user_password.Add(TextCtrl_user_password, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)
        sizer_user_password.Add(bt_pass_help, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        sizer_input.Add(sizer_user_password, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.Bind(wx.EVT_TEXT, lambda evt, textCtr='user_password': self.evt_txt(evt, textCtr), TextCtrl_user_password)  # 事件

        # user_email
        txt_email = wx.StaticText(self, -1, r'邮箱', style=wx.ST_NO_AUTORESIZE)  # 文字
        TextCtrl_user_email = wx.TextCtrl(self, value=self.user_data['user_email'], style=wx.TE_LEFT)  # 输入框
        bt_email_help = wx.Button(self, label='邮箱帮助', size=(100, 25))
        sizer_user_email.Add(txt_email, proportion=0, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        sizer_user_email.Add(TextCtrl_user_email, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)
        sizer_user_email.Add(bt_email_help, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        sizer_input.Add(sizer_user_email, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.Bind(wx.EVT_TEXT, lambda evt, textCtr='user_email': self.evt_txt(evt, textCtr), TextCtrl_user_email)  # 事件

        # 'User-Agent'
        txt_User_Agent = wx.StaticText(self, -1, r'User_Agent', style=wx.ST_NO_AUTORESIZE)  # 文字
        TextCtrl_User_Agent = wx.TextCtrl(self, value=self.user_data['User-Agent'], style=wx.TE_LEFT)  # 输入框
        bt_ua_help = wx.Button(self, label='ua帮助', size=(100, 25))
        sizer_User_Agent.Add(txt_User_Agent, proportion=0, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        sizer_User_Agent.Add(TextCtrl_User_Agent, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)
        sizer_User_Agent.Add(bt_ua_help, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        sizer_input.Add(sizer_User_Agent, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.Bind(wx.EVT_TEXT, lambda evt, textCtr='User—Agent': self.evt_txt(evt, textCtr), TextCtrl_User_Agent)  # 事件

        # ip_port
        txt4_1 = wx.StaticText(self, -1, r'服务器ip', style=wx.ST_NO_AUTORESIZE)  # 文字
        TextCtrl_ip = wx.TextCtrl(self, value=str(self.user_data['server_ip']), style=wx.TE_LEFT)  # 输入框
        txt4_2 = wx.StaticText(self, -1, r'服务器port', style=wx.ST_NO_AUTORESIZE)  # 文字
        TextCtrl_port = wx.TextCtrl(self, value=str(self.user_data['server_port']), style=wx.TE_LEFT)  # 输入框
        bt_ip_port_help = wx.Button(self, label='ip_port帮助', size=(100, 25))
        sizer_ip_port.Add(txt4_1, proportion=0, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        sizer_ip_port.Add(TextCtrl_ip, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)
        sizer_ip_port.Add(txt4_2, proportion=0, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        sizer_ip_port.Add(TextCtrl_port, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)
        sizer_ip_port.Add(bt_ip_port_help, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        sizer_input.Add(sizer_ip_port, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.Bind(wx.EVT_TEXT, lambda evt, textCtr='server_ip': self.evt_txt(evt, textCtr), TextCtrl_ip)  # 事件
        self.Bind(wx.EVT_TEXT, lambda evt, textCtr='server_port': self.evt_txt(evt, textCtr), TextCtrl_port)  # 事件
        
        # user_dormitory
        txt3 = wx.StaticText(self, -1, r'宿舍号', style=wx.ST_NO_AUTORESIZE)  # 文字
        TextCtrl_user_dormitory = wx.TextCtrl(self, value=self.user_data['user_dormitory'], style=wx.TE_LEFT)  # 输入框
        sizer_user_dormitory.Add(txt3, proportion=0, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        sizer_user_dormitory.Add(TextCtrl_user_dormitory, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)
        sizer_input.Add(sizer_user_dormitory, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.Bind(wx.EVT_TEXT, lambda evt, textCtr='user_dormitory': self.evt_txt(evt, textCtr), TextCtrl_user_dormitory)  # 事件
        self.bt_help = wx.Button(self, label='帮助', size=(100, 25))
        sizer_user_dormitory.Add(self.bt_help, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

        # tip_inf
        txt_tip_1 = wx.StaticText(self, -1, u'郑重声明:本程序仅用作学习交流，不用于商业用途。'
                                            u'\n仅适用于对应时段在学校, 身体状况正常的人使用。'
                                            u'\n如有身体上的不适或离开学校,请停止该自动打卡,并如实上报自身情况', style=wx.ST_NO_AUTORESIZE)  # 文字
        txt_tip_2 = wx.StaticText(self, -1, r'源码地址:https://github.com/wzz618/wozaixiaoyuan.git', style=wx.ST_NO_AUTORESIZE)  # 文字
        txt_tip_3 = wx.StaticText(self, -1, r'联系QQ:3574403347', style=wx.ST_NO_AUTORESIZE)  # 文字
        txt_tip_4 = wx.StaticText(self, -1, r'个人网站:http://www.trafficwzz.com/', style=wx.ST_NO_AUTORESIZE)  # 文字
        sizer_tip_inf.Add(txt_tip_1, proportion=0, border=5, flag=wx.ALL)
        sizer_tip_inf.Add(txt_tip_2, proportion=0, border=3, flag=wx.ALL)
        sizer_tip_inf.Add(txt_tip_3, proportion=0, border=3, flag=wx.ALL)
        sizer_tip_inf.Add(txt_tip_4, proportion=0, border=3, flag=wx.ALL)
        sizer_input.Add(sizer_tip_inf, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)


        # 选择界面
        sizer_choise = wx.BoxSizer()
        self.bt_heat1 = wx.Button(self, label='尝试登录', size=(50, 100))

        # 绑定事件
        self.Bind(wx.EVT_BUTTON, self.btn_click, self.bt_heat1)
        self.Bind(wx.EVT_BUTTON, self.btn_chick_help, self.bt_help)
        self.Bind(wx.EVT_BUTTON, self.btn_chick_help, bt_user_help)
        self.Bind(wx.EVT_BUTTON, self.btn_chick_help, bt_ip_port_help)
        self.Bind(wx.EVT_BUTTON, self.btn_chick_help, bt_ua_help)
        self.Bind(wx.EVT_BUTTON, self.btn_chick_help, bt_email_help)
        self.Bind(wx.EVT_BUTTON, self.btn_chick_help, bt_pass_help)

        sizer_choise.Add(self.bt_heat1, proportion=1, flag=wx.ALL, border=5)

        # 帮助界面
        # 组装容器
        sizer.Add(sizer_input, proportion=3, flag=wx.EXPAND | wx.ALL, border=5)
        sizer.Add(sizer_choise, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)

        self.SetAutoLayout(True)  # 自动适应布局
        self.SetSizer(sizer)
        self.Layout()

    def read_config(self):  # 读取文件
        if not os.path.exists(os.path.dirname(self.user_data_path)):  # 如果文件目录不在，则创建目录
            os.mkdir(os.path.dirname(self.user_data_path))
        if not os.path.exists(self.user_data_path):
            f = open(self.user_data_path, 'w+')
            data = data_store.data  # 读入默认的信息模板
            f.write(str(data))
            f.close()
        else:
            with open(self.user_data_path, 'r+') as f:
                data = eval(f.read())
        return data

    def btn_click(self, evt):
        log = log_management.log_management()
        with open(self.user_data_path, 'w+') as f:
            f.write(str(self.user_data))
        # if event.Label == '尝试登录':
        #     wzxy = wozaixiaoyuan.wozaixiaoyuan(log=log)
        #     res = wzxy.login(self.user_data['user_name'], self.user_data['user_password'])
        #     frame_action(self.user_data_path).Show()
        # 输出情况
        wzxy = wozaixiaoyuan.wozaixiaoyuan(log=log)
        res = wzxy.login(self.user_data['user_name'], self.user_data['user_password'])
        if res['code'] == 0:
            frame_action(self.user_data_path).Show()
        else:
            with open(log.document_path, 'r+') as f:
                log_data = f.read()
                dlg = wx.MessageDialog(None, log_data, u'操作提示')  #
                dlg.ShowModal()

    def btn_chick_help(self, evt):
        event = evt.GetEventObject()
        if event.Label == '帮助':
            txt = '源码地址:https://github.com/wzz618/wozaixiaoyuan.git\n联系QQ:3574403347\n' \
                  '如果密码错误，就手机登录我在校园重新修改一次密码再试试\nuser-agent如果不做修改则采用系统的默认值，但是建议把该项改成与手机的相同 '
            dlg = wx.MessageDialog(None, txt, u'操作提示')  #
            dlg.ShowModal()
        elif event.Label == '账号帮助':
            txt = '该项必填，我在校园的账号，默认是手机号，因为不同学校可能会存在相同的学号'
            dlg = wx.MessageDialog(None, txt, u'账号帮助')  #
            dlg.ShowModal()
        elif event.Label == '密码帮助':
            txt = '如果密码错误，则手机打开我在校园客户端修改密码重试'
            dlg = wx.MessageDialog(None, txt, u'密码帮助')  #
            dlg.ShowModal()
        elif event.Label == '邮箱帮助':
            txt = '该项必填，接收打卡状况消息的邮箱'
            dlg = wx.MessageDialog(None, txt, u'邮箱帮助')  #
            dlg.ShowModal()
        elif event.Label == 'ua帮助':
            txt = '该项选填，user-agent包含了手机标识码等必要信息，可以在手机微信打开网址 https://www.ip138.com/useragent/ ，复制对应的信息粘贴上去'
            dlg = wx.MessageDialog(None, txt, u'ua帮助')  #
            dlg.ShowModal()
        elif event.Label == 'ip_port帮助':
            txt = '该项必填，请选择对应学院的端口\n' \
                  '目前支持的服务器ip:  8.141.52.187\n' \
                  '运输工程学院port:   6998\n' \
                  '公路学院port:    6697\n'
            dlg = wx.MessageDialog(None, txt, u'ip_port帮助')  #
            dlg.ShowModal()

    def evt_txt(self, evt, textCtr):
        event = evt.GetEventObject()
        self.user_data[textCtr] = event.Value


class frame_action(wx.Frame):
    def __init__(self, user_data_path):
        self.user_data_path = user_data_path
        self.user_data = eval(open(self.user_data_path, 'r').read())

        wx.Frame.__init__(self, None, -1, '{}系统'.format(data_store.academy[self.user_data['server_port']]),
                          pos=(100, 100), size=(350, 200))
        self.Center()

        # 总容器
        sizer = wx.BoxSizer(wx.VERTICAL)

        #
        sizer_check_time = wx.BoxSizer(wx.VERTICAL)
        sizer_atcion = wx.BoxSizer()

        # sizer_check_time
        bt_check_time = wx.Button(self, label='检查服务的时间', size=(300, 25))
        sizer_check_time.Add(bt_check_time, proportion=1, flag=wx.ALL, border=5)
        sizer.Add(sizer_check_time, proportion=1, flag=wx.ALL, border=5)

        self.Bind(wx.EVT_BUTTON, self.btn_click, bt_check_time)

        # sizer_atcion
        # sizer_atcion_choice
        sizer_atcion_choice = wx.BoxSizer(wx.VERTICAL)
        heat1_radio = wx.CheckBox(self, label='晨检', pos=(0, 20))
        heat2_radio = wx.CheckBox(self, label='午检', pos=(0, 20))
        sign_radio = wx.CheckBox(self, label='签到', pos=(0, 20))

        self.Bind(wx.EVT_CHECKBOX, self.onChecked)

        sizer_atcion_choice.Add(heat1_radio, proportion=1, flag=wx.ALL, border=5)
        sizer_atcion_choice.Add(heat2_radio, proportion=1, flag=wx.ALL, border=5)
        sizer_atcion_choice.Add(sign_radio, proportion=1, flag=wx.ALL, border=5)

        # action
        bt_action = wx.Button(self, label='提交', size=(100, 80))
        self.Bind(wx.EVT_BUTTON, self.btn_click, bt_action)

        sizer_atcion.Add(sizer_atcion_choice, proportion=1, flag=wx.ALL, border=5)
        sizer_atcion.Add(bt_action, proportion=1, flag=wx.ALL, border=5)
        sizer.Add(sizer_atcion, proportion=3, flag=wx.ALL, border=5)

        self.SetAutoLayout(True)  # 自动适应布局
        self.SetSizer(sizer)
        self.Layout()

    def onChecked(self, evt):
        # 把对应的标定为1
        event = evt.GetEventObject()
        index = event.GetLabel()
        if event.GetValue():
            self.user_data[index] = 1
        else:
            self.user_data[index] = 0

    def btn_click(self, evt):
        event = evt.GetEventObject()
        self.user_data['user_action'] = event.Label

        log = log_management.log_management()
        clt = client.Client(log=log)
        res = clt.send_inf(self.user_data, ip_port=(self.user_data['server_ip'], int(self.user_data['server_port'])))
        dlg = wx.MessageDialog(None, res, u'操作提示')  #
        dlg.ShowModal()


class App(wx.App):
    def __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        super().__init__(redirect, filename, useBestVisual, clearSigInt)
        self.frame = None

    def OnInit(self):
        # 创建窗口对象
        self.frame = frame()
        self.frame.Show()
        return True

    def OnExit(self):
        return 0


if __name__ == '__main__':
    # print(os.path.abspath(os.path.dirname(os.getcwd())))
    app = App()  # 创建自定以对象App
    app.MainLoop()  # 进入事件主循环


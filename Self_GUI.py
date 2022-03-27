import wx
import os
import wozaixiaoyuan
import log_management


class frame(wx.Frame):
    def __init__(self):
        self.user_data_path = r'系统日志/user_data.txt'
        self.user_data = self.read_config()

        # 定义容器
        wx.Frame.__init__(self, None, -1, '我在校园自助签到系统', pos=(100, 100), size=(400, 250))
        self.Center()

        # 总容器
        sizer = wx.BoxSizer(wx.VERTICAL)

        # 输入界面
        sizer_input = wx.BoxSizer(wx.VERTICAL)
        sizer_user_name = wx.BoxSizer()
        sizer_user_password = wx.BoxSizer()
        sizer_user_dormitory = wx.BoxSizer()
        # 捆绑按钮
        # sizer_user_name
        txt1 = wx.StaticText(self, -1, r'账号', style=wx.ST_NO_AUTORESIZE)  # 文字
        TextCtrl_user_name = wx.TextCtrl(self, value=self.user_data['user_name'], style=wx.TE_LEFT)  # 输入框
        self.Bind(wx.EVT_TEXT, lambda evt, textCtr='账号': self.evt_txt(evt, textCtr), TextCtrl_user_name)  # 事件

        sizer_user_name.Add(txt1, proportion=0, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        sizer_user_name.Add(TextCtrl_user_name, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)
        sizer_input.Add(sizer_user_name, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)

        # user_password
        txt2 = wx.StaticText(self, -1, r'密码', style=wx.ST_NO_AUTORESIZE)  # 文字
        TextCtrl_user_password = wx.TextCtrl(self, value=self.user_data['user_password'], style=wx.TE_LEFT)  # 输入框
        sizer_user_password.Add(txt2, proportion=0, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        sizer_user_password.Add(TextCtrl_user_password, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)
        sizer_input.Add(sizer_user_password, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.Bind(wx.EVT_TEXT, lambda evt, textCtr='密码': self.evt_txt(evt, textCtr), TextCtrl_user_password)  # 事件

        # user_dormitory
        txt3 = wx.StaticText(self, -1, r'宿舍号', style=wx.ST_NO_AUTORESIZE)  # 文字
        TextCtrl_user_dormitory = wx.TextCtrl(self, value=self.user_data['user_dormitory'], style=wx.TE_LEFT)  # 输入框
        sizer_user_dormitory.Add(txt3, proportion=0, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        sizer_user_dormitory.Add(TextCtrl_user_dormitory, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)
        sizer_input.Add(sizer_user_dormitory, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.Bind(wx.EVT_TEXT, lambda evt, textCtr='宿舍号': self.evt_txt(evt, textCtr), TextCtrl_user_dormitory)  # 事件
        self.bt_help = wx.Button(self, label='帮助', size=(25, 25))
        sizer_user_dormitory.Add(self.bt_help, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)



        # 选择界面
        sizer_choise = wx.BoxSizer()
        self.bt_heat1 = wx.Button(self, label='晨检', size=(50, 100))
        self.bt_heat2 = wx.Button(self, label='午检', size=(50, 100))
        self.bt_sign = wx.Button(self, label='签到', size=(50, 100))

        # 绑定事件
        self.Bind(wx.EVT_BUTTON, self.btn_click, self.bt_heat1)
        self.Bind(wx.EVT_BUTTON, self.btn_click, self.bt_heat2)
        self.Bind(wx.EVT_BUTTON, self.btn_click, self.bt_sign)
        self.Bind(wx.EVT_BUTTON, self.btn_chick_help, self.bt_help)

        sizer_choise.Add(self.bt_heat1, proportion=1, flag=wx.ALL, border=5)
        sizer_choise.Add(self.bt_heat2, proportion=1, flag=wx.ALL, border=5)
        sizer_choise.Add(self.bt_sign, proportion=1, flag=wx.ALL, border=5)

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
            data = {
                'user_name': '请输入你的账号',
                'user_password': '请输入你的密码',
                'user_dormitory': '请输入你的宿舍号码'
            }
            f.write(str(data))
            f.close()
        else:
            with open(self.user_data_path, 'r+') as f:
                data = eval(f.read())
        return data

    def btn_click(self, evt):
        event = evt.GetEventObject()
        log = log_management.log_management()
        log.write_data('正在传递信息')
        wzxy = wozaixiaoyuan.wozaixiaoyuan(log=log)
        wzxy.login(self.user_data['user_name'], self.user_data['user_password'])
        with open(self.user_data_path, 'w+') as f:
            f.write(str(self.user_data))
        if event.Label == '晨检':
            wzxy.heat(seq=1)
        elif event.Label == '午检':
            wzxy.heat(seq=2)
        elif event.Label == '签到':
            wzxy.sign()
        # 输出情况
        with open(log.document_path, 'r+') as f:
            log_data = f.read()
            dlg = wx.MessageDialog(None, log_data, u'操作提示')  #
            dlg.ShowModal()

    def btn_chick_help(self, evt):
        event = evt.GetEventObject()
        if event.Label == '帮助':
            txt = '源码地址:https://github.com/wzz618/wozaixiaoyuan.git\n联系QQ:3574403347'
            dlg = wx.MessageDialog(None, txt, u'操作提示')  #
            dlg.ShowModal()

    def evt_txt(self, evt, textCtr):
        event = evt.GetEventObject()
        if textCtr == '账号':
            self.user_data['user_name'] = event.Value
        elif textCtr == '密码':
            self.user_data['user_password'] = event.Value
        elif textCtr == '宿舍号':
            self.user_data['user_dormitory'] = event.Value


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
    app = App()  # 创建自定以对象App
    app.MainLoop()  # 进入事件主循环

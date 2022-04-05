import requests
import json
import time


class wozaixiaoyuan:
    def __init__(self, session_parent=None, log=None):
        self.session_parent = session_parent  # 登录的session
        if session_parent is None:
            self.session = requests.session()
        else:
            self.session = session_parent
        self.cookies = None

        self.log = log  # 日志对象

    def login(self, username, password):  # 登入账号，更新系统的session
        login_url = 'https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username'  # 目标网址
        login_data = {
            'username': username,
            'password': password
        }  # 登录账号和密码
        login_headers = {
            'Host': 'gw.wozaixiaoyuan.com',
            'Connection': 'keep-alive',
            'Content-Length': '2',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI '
                          'MiniProgramEnv/Windows WindowsWechat',
            'Content-Type': 'application/json;charset=UTF-8',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-us,en'
        }  # 表单的表头
        login_url = "{0}?username={1}&password={2}".format(login_url, str(login_data['username']),
                                                           str(login_data['password']))  # 通过 url 的 '？' 方法写入参数  # 更新url
        res = self.session.post(url=login_url, headers=login_headers, data='{}')
        try:
            if json.loads(res.text)['code'] == 0:  # 返回值是0，说明登录成功，保留系统分配的JWSESSION，大致够用半个月，然后系统就会取消自动分配的JW..
                self.session.cookies.set('JWSESSION', res.headers['JWSESSION'])  # 更新JWSESSION值
                self._print('登录成功：{}'.format(json.loads(res.text)))
            else:
                self._print('登录失败：{}'.format(json.loads(res.text)))
            return json.loads(res.text)
        except Exception as E:
            self._print('登录错误：{}'.format(E))

    def get_HeatUsers(self, seq=1):
        """

        :param seq: int 日期
        :return: list 未检查的人员名单
        """
        # seq 1, 2, 3 分别对应晨检、午检、晚检
        # 班级日检日报的信息
        getHeatUsers_url = 'https://student.wozaixiaoyuan.com/heat/getHeatUsers.json'
        getHeatUsers_headers = {
            'Host': 'student.wozaixiaoyuan.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI '
                          'MiniProgramEnv/Windows WindowsWechat',
            'content-type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        getHeatUsers_data = {'seq': str(seq), 'date': str(time.strftime("%Y%m%d")), 'type': '0'}  # 测试用的，后边程序会更改

        not_heat_names_list = []  # 不签到的人

        try:
            res = self.session.post(url=getHeatUsers_url, headers=getHeatUsers_headers,
                                    data=getHeatUsers_data)
            if json.loads(res.text)['code'] == 0:  # 检查是否请求成功且正确
                # print('{}\t成功获得班级成员日检日报信息'.format(time.strftime("%H:%M:%S")))
                data = json.loads(res.text)['data']  # 观察是否有不晨检的同学
                if len(data) != 0:
                    for inf in data:  # 如果有，则更新不晨检列表
                        name = inf['name']
                        not_heat_names_list.append(name)
                    self._print('未完成日检日报的班级成员为{}'.format(not_heat_names_list))
                    return not_heat_names_list
                else:
                    self._print('班级成员全部完成日检日报')
            else:
                self._print('获得班级成员日检日报信息失败：{}'.format(json.loads(res.text)['message']))  # 输出登录错误的错误原因
        except Exception as E:
            self._print('获得班级成员日检日报信息失败：{}'.format(E))  # 输出登录错误的错误原因

    def get_SignResult(self):
        # 获取当天的签到 id 值
        # 校区签到的列表
        getList_url = 'https://student.wozaixiaoyuan.com/gradeManage/sign/getList.json'
        getList_headers = {
            'Host': 'student.wozaixiaoyuan.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI '
                          'MiniProgramEnv/Windows WindowsWechat',
            'content-type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        getList_date = {
            'keyword': '',
            'page': '1'
        }
        # 校区签到的班级成员情况
        getSignResult_url = 'https://student.wozaixiaoyuan.com/gradeManage/sign/getSignResult.json'
        getSignResult_headers = {
            'Host': 'student.wozaixiaoyuan.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI '
                          'MiniProgramEnv/Windows WindowsWechat',
            'content-type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        getSignResult_data = {
            'id': ''
        }
        try:
            res = self.session.post(url=getList_url, headers=getList_headers,
                                    data=getList_date)
            if json.loads(res.text)['data'][0]['end'].split(' ')[0] == time.strftime("%Y-%m-%d"):  # 判断第一个签到是不是当天的签到
                getSignResult_data['id'] = json.loads(res.text)['data'][0]['id']  # 如果判断成功，则更新 查询签到的id
                res = self.session.post(url=getSignResult_url, headers=getSignResult_headers,  # 查询签到
                                        data=getSignResult_data)
                data = json.loads(res.text)['data']
                not_sign_names_list = []
                if len(data['notSign']) != 0:  # 判断是否有成员不签到
                    for inf in data['notSign']:
                        name = inf['name']
                        not_sign_names_list.append(name)
                    self._print('未完成签到的班级成员为{}'.format(not_sign_names_list))
                    return not_sign_names_list
                else:
                    self._print('班级成员全部完成签到')
        except Exception as E:
            print('获得班级成员签到信息失败:{}'.format(E))

    def get_HealthResult(self):
        # 健康打卡的成员情况
        get_HealthResult_url = 'https://student.wozaixiaoyuan.com/health/getHealthUsers.json'
        get_HealthResult_headers = {
            'Host': 'student.wozaixiaoyuan.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI '
                          'MiniProgramEnv/Windows WindowsWechat',
            'content-type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        get_HealthResult_data = {
            'type': '0',
            'date': str(time.strftime("%Y%m%d"))
        }
        # 获取当天的日期
        try:
            res = self.session.post(url=get_HealthResult_url, headers=get_HealthResult_headers,
                                    data=get_HealthResult_data)
            data = json.loads(res.text)['data']
            not_health_names_list = []
            if len(data) != 0:  # 判断是否有成员不签到
                for inf in data:
                    name = inf['name']
                    not_health_names_list.append(name)
                self._print('未完成健康打卡的班级成员为{}'.format(not_health_names_list))
                return not_health_names_list
            else:
                self._print('班级成员全部完成健康打卡')
        except Exception as E:
            self._print('获得班级成员健康打卡信息失败{}'.format(E))

    def health(self, dormitory_name):  # 健康打卡
        """
        实现健康打卡
        :param dormitory_name: string 宿舍号，楼号#宿舍号
        :return: None
        """
        health_url = 'https://student.wozaixiaoyuan.com/health/save.json'
        health_headers = {
            'Host': 'student.wozaixiaoyuan.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI '
                          'MiniProgramEnv/Windows WindowsWechat',
            'content-type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        health_data = {
            'answers': '["0","长安大学渭水校区{}","1","{}","36.0","没有","1","1","2"]'.format(dormitory_name, dormitory_name),
            'latitude': '34.29318',
            'longitude': '108.94712',
            'country': '中国',
            'city': '西安市',
            'district': '未央区',
            'province': '陕西省',
            'township': '张家堡街道',
            'street': '未央路',
            'areacode': '610112'
        }
        try:
            res = self.session.post(url=health_url, headers=health_headers, data=health_data)
            if json.loads(res.text)['code'] == 0:
                self._print('健康打卡成功')
            else:
                self._print('健康打卡失败：{}'.format(json.loads(res.text)['message']))
        except Exception as E:
            self._print('健康打卡错误:{}'.format(E))

    def heat(self, seq=1):  # 日检日报
        """
        实现日检日报
        :param seq: int 早、中、晚分别对应1、2、3
        :return: None
        """
        heat_url = 'https://student.wozaixiaoyuan.com/heat/save.json'
        heat_headers = {
            'Host': 'student.wozaixiaoyuan.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI '
                          'MiniProgramEnv/Windows WindowsWechat',
            'content-type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        heat_data = {
            'answers': '["0","无"]',
            'seq': '{}'.format(seq),
            'temperature': '36.1',
            'latitude': '34.29318',
            'longitude': '108.94712',
            'country': '中国',
            'city': '西安市',
            'district': '未央区',
            'province': '陕西省',
            'township': '张家堡街道',
            'street': '未央路',
            'areacode': '610112'
        }
        try:
            res = self.session.post(url=heat_url, headers=heat_headers, data=heat_data)
            if json.loads(res.text)['code'] == 0:
                self._print('日检日报成功')
            else:
                self._print('日检日报失败：{}'.format(json.loads(res.text)['message']))
        except Exception as E:
            self._print('日检日报错误{}'.format(E))

    def sign(self):
        # 签到进入界面，目的是获得对应的id
        getSignMessage_url = 'https://student.wozaixiaoyuan.com/sign/getSignMessage.json'
        getSignMessage_headers = {
            'Host': 'student.wozaixiaoyuan.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI '
                          'MiniProgramEnv/Windows WindowsWechat',
            'content-type': 'application/x-www-form-urlencoded',  # 注意，这个不是application/json
            'Accept-Encoding': 'gzip, deflate, br'
        }
        getSignMessage_data = {
            "page": "1",
            "size": "5"
        }
        # 签到的post信息
        sign_url = 'https://student.wozaixiaoyuan.com/sign/doSign.json'
        sign_headers = {
            'Host': 'student.wozaixiaoyuan.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI '
                          'MiniProgramEnv/Windows WindowsWechat',
            'content-type': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        sign_data = '{"id": "id_num","signId": "signId_num", "latitude": "34.2931800000","longitude": ' \
                    '"108.9471200000", ' \
                    '"country": "中国","province": "陕西省","city": "西安市","district": "问远路","township": "汉城街道"} '
        # 必须用字符串，传入的data只认二进制。
        # 用str()转化字典，会存在转义字符，两种的二进制代码不同
        try:
            res = self.session.post(url=getSignMessage_url, headers=getSignMessage_headers, data=getSignMessage_data)
            if json.loads(res.text)['code'] == 0:
                SignMessage_date = json.loads(res.text)['data'][0]['end'].split(' ')[0]  # 获得最新的签到信息
                if time.strftime("%Y-%m-%d") == SignMessage_date:  # 如果最新的签到信息是当天的
                    # 获得当天的签到信息
                    id = json.loads(res.text)['data'][0]['id']
                    logId = json.loads(res.text)['data'][0]['logId']
                    # 更新签到信息
                    sign_data = sign_data.replace("id_num", logId)
                    sign_data = sign_data.replace("signId_num", id)
                    sign_data = str(sign_data).encode('utf-8')
                    self._print('成功获得当天的签到信息')
                    try:
                        res = self.session.post(url=sign_url, headers=sign_headers, data=sign_data)
                        if json.loads(res.text)['code'] == 0:
                            self._print('签到成功')
                        else:
                            self._print('签到失败：{}'.format(json.loads(res.text)['message']))
                    except Exception as E:
                        self._print('签到错误{}'.format(E))
                else:
                    self._print('当天的签到未开始')
            else:
                self._print('日检日报失败：{}'.format(json.loads(res.text)['message']))
        except Exception as E:
            self._print('尝试从SignMessage页面获得签到信息错误{}'.format(E))

    def _print(self, inf):
        # 重写了下输出
        if self.log is not None:
            self.log.write_data(inf)
            print(str(time.strftime("%H:%M:%S")) + '\t' + inf)
        else:
            print(str(time.strftime("%H:%M:%S")) + '\t' + inf)


if __name__ == '__main__':
    with open('系统日志/admin.txt', 'r', encoding='UTF-8') as f:
        admin = eval(f.read())
    aa = wozaixiaoyuan()
    aa.login(admin['username'], admin['password'])
    aa.sign()

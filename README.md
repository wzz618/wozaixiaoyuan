# wozaixiaoyuan
我在校园的各项签到接口和信息，已经班委自动提醒的实现
# wozaixiaoyuan.py
我在校园的接口对象
通过登录账号实现自动打卡和签到
查询账号权限下，可以看到的未签到名单（班委自动提醒）
## login(self, username, password)
登入账号，更新系统的session
## get_HeatUsers(self, seq=1)
:param seq: int 日期
:return: list 日检日报的人员名单
## get_SignResult(self)
获得未签到的人员名单
## get_HealthResult(self)
## health(self, dormitory_name)
## heat(self, seq=1)
## sign(self)

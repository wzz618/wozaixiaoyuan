西安疫情市区解封，但是依旧封闭学校，而且要求每天两检和签到（封校定个鬼位置）。并且把结果和德育实践分以及班级各项评优指标挂钩，所以基于对我在校园的抓包，编写了一套自动签到和打卡系统，外加班委的自动督促提醒。
该代码基于长安大学运输学院19级的我在校园各项抓包对应编写，不同学校的人可以根据自己的需求下载更改。
希望有同好一起完善信息。
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
获得未健康打卡的人员名单
## health(self, dormitory_name)
健康打卡的接口
## heat(self, seq=1)
日检日报的接口
## sign(self)
签到的接口

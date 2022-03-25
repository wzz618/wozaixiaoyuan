西安疫情市区解封，但是依旧封闭学校，而且要求每天两检和签到（封校定个鬼位置）。  
并且把结果和德育实践分以及班级各项评优指标挂钩，所以基于对我在校园的抓包，编写了一套自动签到和打卡系统，外加班委的自动督促提醒。  
该代码基于长安大学运输学院19级的我在校园各项抓包对应编写，不同学校的人可以根据自己的需求下载更改。
希望有同好一起完善信息。
## wozaixiaoyuan.py ##
**需要填写'/系统日志/admin.txt'中对应的键值**
- 我在校园的接口对象，通过抓包找到的对应API
- 通过登录账号实现自动打卡和签到
- 查询账号权限下，可以看到的未签到名单（班委自动提醒）
> class wozaixiaoyuan:
>> ### login(self, username, password)
>>>登入账号，更新系统的session
>> ### get_HeatUsers(self, seq=1)
>>>:param seq: int 日期  
>>>:return: list 日检日报的人员名单
>> ### get_SignResult(self)
>>>获得未签到的人员名单
>> ### get_HealthResult(self)
>>> 获得未健康打卡的人员名单
>> ### health(self, dormitory_name)
>>>健康打卡的接口
>> ### heat(self, seq=1)
>>> 日检日报的接口
>>### sign(self)
>>> 签到的接口
## tip_system.py ##
- 班委提醒系统，用来提醒班级里面没有打卡的人
- 自我偷懒系统  
**需要填写的文件如下**
- 系统日志/admin.txt
- 系统日志/admin_data.txt
- 系统日志/email_data.txt
- 系统日志/tip_time.txt
- 用户信息/班级成员信息.xlsx
> class tip_system
>> ## read_config(self)
>>> 读取配置文件
>> ## in_tips_time(self)
>>> 判断是否在提醒时间
>> ## Run(self)
>>> 运行
## log_management ##
- 自己编写的日志系统，用来存储日志
## send_email.py ## 
**需要填写'/系统日志/admin.txt'中的邮箱信息**
- 自己编写的邮箱系统，用来发送提醒信息
- 其中的邮箱依赖用的是自己域名的邮箱代理


import time
import wozaixiaoyuan

second_delays = 3 * 120  # 秒数的延误最大值，提供一定的误差区间


def auto_tip_check(tip_time):
    """
    提醒检查
    :param tip_time: dict 提醒的时间
    :return:
        tip_type: string 提醒的类型
        time_loc: int 提醒的时间在对应列表中的位置
        sleep_time: string 需要睡眠的时间"%H:%M:%S"
    """
    now_time = time.strftime("%H:%M:%S")
    now_time_s = seconds(now_time)
    tip_type = None  # 目前的提醒类型
    # 获得提醒的类型
    for key in tip_time:
        first_tip_time = tip_time[key][0]
        last_tip_time = tip_time[key][-1]
        if seconds(first_tip_time) <= now_time_s <= seconds(last_tip_time) + second_delays:
            tip_type = key
            break
    # 获得提醒时间在列表中的排序位置
    if tip_type is not None:
        dis_time = None
        time_loc = 0
        for i in range(len(tip_time[tip_type])):
            new_dis_time = abs(seconds(tip_time[tip_type][i]) - seconds(now_time))  # 相差的时间
            if dis_time is None:
                dis_time = new_dis_time
            else:
                if dis_time >= new_dis_time:
                    dis_time = new_dis_time  # 更新最短间隔和位置
                    time_loc = i
                else:
                    break
    else:
        time_loc = 0
    # 获得下一次提醒的时间
    tip_time_list = []
    for key in tip_time:
        for time_inf in tip_time[key]:
            tip_time_list.append(seconds(time_inf))  # 转化为s
    tip_time_list = sorted(tip_time_list)  # 排序

    if now_time_s > tip_time_list[-1] - second_delays:
        # 如果超过当天的提醒时间
        sleep_time = 24 * 60 * 60 + tip_time_list[0] - now_time_s
    else:
        # 如果未超过当天的提醒时间
        for i in range(len(tip_time_list)):
            # 找到第一个大于当前时间的下一次提醒时间
            if tip_time_list[i] > now_time_s:
                sleep_time = tip_time_list[i] - now_time_s
                break
    sleep_time = to_StrTime(sleep_time)
    return tip_type, time_loc, sleep_time


def get_unfinished_list(wzxy, tip_type):  # 获得提醒类型
    if tip_type == '晨检':
        return wzxy.get_HeatUsers(seq=1)
    elif tip_type == '午检':
        return wzxy.get_HeatUsers(seq=2)
    elif tip_type == '签到':
        return wzxy.get_SignResult()


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
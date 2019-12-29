# -*- coding: utf-8 -*-
# @Time : 2019/9/5 10:26
# @Author : Syu
import controler
import sys
import time


# 常规录屏功能测试，开始暂停继续结束
def test_1(params):
    controler.start(params)
    time.sleep(10)  # 开始录10秒
    controler.pause(params)
    time.sleep(4)  # 暂停4秒
    controler.carry_on(params)
    time.sleep(10)  # 继续录10秒
    controler.end(params)  # 所录视频应为20秒


# 定时录屏功能测试
def test_2(params):
    controler.start_timing(params)


if __name__ == '__main__':
    params = {}
    params['timing_time'] = 0.1  # 定时时长(min)
    params['save_path'] = sys.path[0]  # 保存路径
    params['end_time'] = 0.1  # 录屏最长时长(hours)
    # test_1(params)
    # test_2(params)


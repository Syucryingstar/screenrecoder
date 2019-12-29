# -*- coding: utf-8 -*-
# @Time : 2019/8/11 14:44
# @Author : Syu
import socket
import json
import sys
import time
from threading import Thread
from PIL import ImageGrab
import cv2
import numpy as np
import pyautogui as pag

status = 'start'  # 录屏状态的全局变量
timeout = float(sys.argv[1])
path = sys.argv[2]  # 保存路径
codec = sys.argv[3]  # 视频编码


# 录屏状态服务
def open_server():
    global path, status
    try:
        sock = socket.socket(type=socket.SOCK_DGRAM)
        sock.bind(('127.0.0.1', 3344))  # 绑定地址
        # 实现通信循环
        while True:
            data, addr = sock.recvfrom(1024)
            data = data.decode('utf-8')
            data = json.loads(data)
            # 接收save_path
            if 'path' in data.keys():
                path = data['path']
            # 接收状态指令
            status = data['status']
            if status == 'end':
                break
        sock.close()
    except Exception as e:
        status = 'end'
        return e


# 创建socket服务的线程
open_server_thread = Thread(target=open_server)
open_server_thread.start()
print("open_server_thread线程开启")


# 发送指令給open_server
def send_message(message: dict):
    try:
        sock = socket.socket(type=socket.SOCK_DGRAM)
        sock.connect(('127.0.0.1', 3344))
        messages = json.dumps(message).encode('utf-8')
        sock.sendto(messages, ('127.0.0.1', 3344))
        sock.close()
    except Exception as e:
        print(e)
        return e


# 最大录屏时间控制(定时、超时)
def monitor():
    global timeout, status
    start_time = time.time()
    while True:
        now_time = time.time()
        if now_time - start_time > timeout:
            break
        elif status == 'end':
            break
        time.sleep(1)
    send_message({'status': 'end'})
    status = 'end'


# 创建监听的线程
monitor_thread = Thread(target=monitor)
monitor_thread.start()
print("monitor_thread线程开启")


# 录屏
def screen_recorder():
    px = ImageGrab.grab()  # 获取全屏信息
    width, high = px.size  # 获得当前屏幕的大小
    fps = 18  # 录屏帧数
    fourcc = cv2.VideoWriter_fourcc(*'{}'.format(codec))  # 录屏文件的编码格式
    video = cv2.VideoWriter(path, fourcc, fps, (width, high))
    frame_count = 0  # 该视频的总帧数
    delay_time = 0
    while True:
        start_time = time.time()
        if status == 'end':
            print("所录帧数:", frame_count, "时间误差:", delay_time)
            break
        elif status == 'start':
            for i in range(0, 3):
                frame_count += 1
                m, n = pag.position()  # 鼠标坐标
                im = ImageGrab.grab()  # 每次运行到这里才能获取一帧画面
                img = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)  # 转为opencv的BGR格式
                # 绘制光标
                boundary_1 = np.array([
                    [m + 1, n + 2], [m + 1, n + 15], [m + 4, n + 12], [m + 6, n + 14], [m + 6, n + 15], [m + 7, n + 16],
                    [m + 7, n + 17], [m + 8, n + 17], [m + 8, n + 16], [m + 7, n + 15], [m + 7, n + 14],
                    [m + 6, n + 13],
                    [m + 6, n + 11], [m + 10, n + 11]
                ])
                boundary_2 = np.array([
                    [m + 0, n + 0], [m + 0, n + 16], [m + 1, n + 16], [m + 4, n + 13], [m + 5, n + 14], [m + 5, n + 15],
                    [m + 6, n + 16], [m + 6, n + 17], [m + 7, n + 18], [m + 8, n + 18], [m + 9, n + 17],
                    [m + 9, n + 16],
                    [m + 8, n + 15], [m + 8, n + 14], [m + 7, n + 13], [m + 7, n + 12], [m + 11, n + 12],
                    [m + 11, n + 11]
                ])
                cv2.fillPoly(img, [boundary_1], (255, 255, 255), 1)  # 光标底色
                cv2.polylines(img, [boundary_2], 1, (0, 0, 0))  # 光标边界
                video.write(img)  # 写入缓存
            end_time = time.time()
            deal_time = 1 / 6 - (end_time - start_time) + delay_time  # 一秒计算6次，一次录3帧，即fps = 18
            # 计算平均每3帧时间与生成每3帧图片所用的时间的差(平均-实际)
            if deal_time > 0:
                # 若差大于平均每帧所用时间(实际处理快了)，则暂停至平均时间才进入下一帧的生成
                time.sleep(deal_time)
                delay_time = 0
            elif deal_time < 0:
                # 若差小于平均每帧所用时间，则赋值给delay_time并在下一次的暂停中减少相应的暂停时间
                delay_time = deal_time


screen_recorder()

# -*- coding: utf-8 -*-
# @Time : 2019/8/11 14:44
# @Author : WangS
import socket
import json
import time
import sys
import os
import subprocess
import traceback

dir_path = sys.path[0]
save_path = ''

'''
选择'XVID'则不需要dll
若选择'X264'则需要复制openh264-1.8.0-win32.dll到C:\Windows\SysWOW64\，具体请参阅README.md
'''


# uiauto的运行权限不足，故本插件在cmd中调用shell.vbs，获取管理员权限的cmd，然后在管理员cmd中调用执行录屏脚本的bat文件
def run_admin_cmd(cmd, timeout=10):
    # 创建执行录屏脚本的bat文件
    f = None
    try:
        bat = sys.path[0] + r"\cmd_command.bat"
        if os.path.isfile(bat):
            os.remove(bat)
        f = open(bat, 'w')
        f.write(cmd)
    except Exception as e:
        traceback.print_exc()
        raise e
    finally:
        if f:
            f.close()
    # 调用shell.vbs开启管理员权限的cmd执行bat
    try:
        shell = sys.path[0] + r"\administrator_cmd.vbs"
        st = subprocess.STARTUPINFO
        st.dwFlags = subprocess.STARTF_USESHOWWINDOW
        st.wShowWindow = subprocess.SW_HIDE
        sp = subprocess.Popen(
            shell,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("[PID] %s: %s" % (sp.pid, cmd))
        sp.wait(timeout=timeout)
        stderr = str(sp.stderr.read().decode("gbk")).strip()
        stdout = str(sp.stdout.read().decode("gbk")).strip()
        if "" != stderr:
            raise Exception(stderr)
        if stdout.find("失败") > -1:
            raise Exception(stdout)
    except Exception as e:
        raise e


# 发送指令給screenrecorder_server.py
def send_message(message: dict):
    try:
        sock = socket.socket(type=socket.SOCK_DGRAM)
        sock.connect(('127.0.0.1', 3344))
        messages = json.dumps(message).encode('utf-8')
        sock.sendto(messages, ('127.0.0.1', 3344))
        sock.close()
        print("发送成功")
    except Exception as e:
        print(e)
        return e


# 初始化配置
def initialization(params):
    # 保存路径判断
    global save_path
    if 'save_path' in params.keys():
        if params['save_path']:
            dir = params['save_path']
    else:
        dir = dir_path
    try:
        video_dir = os.path.join(dir, 'video\\' + time.strftime("%F"))
        # 不存在则创建目录
        if not os.path.exists(video_dir):
            os.makedirs(video_dir)
        save_path = video_dir + "\\" + time.strftime("%F_%H_%M_%S") + '.mkv'
    except:
        print('save_path creation failed')
        return 'save_path creation failed'
    # 复制编码库文件l
    if params['codec'] == 'X264':
        move_dll_cmd = str(sys.executable) + " " + dir_path + "\\move_dll.py"
        dll32_path = r'C:\Windows\SysWOW64\openh264-1.8.0-win32.dll'
        dll64_path = r'C:\Windows\System32\openh264-1.8.0-win64.dll'
        # 若不存在dll则复制dll
        if not os.path.isfile(dll32_path) or not os.access(dll64_path, os.F_OK):
            run_admin_cmd(move_dll_cmd)  # 使用管理员权限运行move_dll.py
            print("移动dll成功")
        time.sleep(0.5)  # 等待dll移动完成
    print("save_path create in:", save_path)
    return "save_path create in:" + save_path


# 开始录屏
def start(params):
    end_time = float(params['end_time']) * 3600  # end_time(h)转换为秒数
    initialization(params)  # 初始化配置
    # 构造cmd命令运行screenrecorder_server:
    cmd_command = str(sys.executable) + " " + dir_path + "\\screenrecorder_server.py {} {} {}".format(
        end_time, save_path, params['codec'])
    run_admin_cmd(cmd_command)
    return "Screenrecorder Start"


# 暂停录屏
def pause(params):
    send_message({'status': 'pause'})
    return "Screenrecorder Pause"


# 继续录屏
def carry_on(params):
    send_message({'status': 'start'})
    return "Screenrecorder Pause"


# 结束录屏
def end(params):
    send_message({'status': 'end'})
    return "Screenrecorder Pause"


# 定时录屏
def start_timing(params):
    end_time = float(params['end_time']) * 3600  # end_time(h)转换为秒数
    initialization(params)  # 初始化配置
    print("启动定时")
    timing_time = float(params['timing_time']) * 60  # time(min)转换为秒数
    if timing_time < end_time:
        end_time = timing_time  # 若定时时长小于最大录屏时长，则定时结束，反之则取最大录屏时长结束
    print("录屏定时为", params['timing_time'], 'min')
    # 构造cmd命令运行timing_server:
    cmd_command = str(sys.executable) + " " + \
                  dir_path + "\\timing_server.py {} {} {}".format(end_time, save_path, params['codec'])
    run_admin_cmd(cmd_command)  # 使用管理员权限运行TimingServer.py
    return "Timing Screenrecorder Start"


if __name__ == '__main__':
    params = {}
    params['codec'] = 'X264'  # 'XVID'
    params['timing_time'] = 0.2  # 定时时长(min)
    # params['action'] = 'start'
    params['save_path'] = sys.path[0]  # 当前路径
    params['end_time'] = 1  # 录屏最长时长1h，防止忘记停止
    start_timing(params)  # 定时录屏
    # send_message({'status': 'pause'})  # , 'path': 'D:/Desktop/test.mkv'})
    # time.sleep(10)
    # send_message({'status': 'start', 'path': 'e.mkv'})
    # send_message({'status': 'end'})
    # time.sleep(21)
    # end(params)


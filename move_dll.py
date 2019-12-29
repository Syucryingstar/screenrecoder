# -*- coding: utf-8 -*-
# @Time : 2019/8/21 22:14
# @Author : Syu

import shutil
import sys
# dll下载地址：https://github.com/cisco/openh264/releases
# 注意python位数
# 32位的python要把dll放C:\Windows\SysWOW64\，64位则放C:\Windows\System32\

dll32_path = sys.path[0] + '\\openh264-1.8.0-win32.dll'
dll64_path = sys.path[0] + '\\openh264-1.8.0-win64.dll'
cope32_path = r'C:\Windows\SysWOW64\openh264-1.8.0-win32.dll'
cope64_path = r'C:\Windows\System32\openh264-1.8.0-win64.dll'
try:
    shutil.copyfile(dll32_path, cope32_path)
    shutil.copyfile(dll64_path, cope64_path)
    print("移动完成")
except Exception as e:
    print("移动失败", e)


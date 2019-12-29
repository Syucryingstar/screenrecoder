### 测试文件为test.py

### 录屏的两种模式
常规录屏: 由指令控制录屏操作(开始、结束、暂停、继续)
定时录屏: 预先设定好录屏时长，不受指令控制，一旦开始只有等时间到了才结束

### 关于编码params["codec"]
XVID编码不需要额外的dll，但所录的视频体积较大（1h时长大约1GB）
X264编码能最大限度压缩视频文件大小而清晰度不变（1h时长大约100+MB），但需要额外dll支持

录屏启动后可开启cmd弹窗供测试使用
把administrator_cmd.vbs中的
shell.ShellExecute path,"","","runas",0
改成
shell.ShellExecute path,"","","runas",1





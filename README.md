# DGLabRandomList
郊狼好玩喵~ 键盘按键触发式随机播放列表生成器~
----

可以根据按键输入随机生成播放列表曲目，可随机的内容有：通道，波形（需要预先设置波形列表，支持DIY），强度，时间

因为这种玩法大家喜欢的波形/道具都因人而异，所以这里以A通道环，B通道塞为蓝本，有需求的可以自行修改代码以匹配自己的玩法。

默认按键：q：低强度随机 
         w：中强度随机 
         e：中高强度随机 
         r：高强度随机 
         t：最后冲刺 
         o或者回车键：30分钟项目，每五分钟提高一次随机等级
         p或者小键盘+号键：60分钟项目，每400秒提高一次随机等级

本程序必须在电脑上运行，你至少需要一台Windows系统的电脑，其他系统没有测试，理论上linux应该可以用

从零开始的安装教程见这里 [DGLabMouseListener2](https://github.com/nobody-x-j/DGLabMouseListener2)

安装完毕之后只需要执行以下步骤：

step 0：使用vscode下载代码

1. 打开miniconda3（windows 10用户可以在开始菜单栏边上搜索miniconda3，然后点击打开），在弹出的Miniconda3框中输入 code，也可以在开始菜单栏边上搜索vscode

```shell
code
```

![image](https://github.com/nobody-x-j/images/blob/main/code.png)

之后会弹出以下界面：

![image](https://github.com/nobody-x-j/images/blob/main/vscode_starting.png)

2. 选择 打开文件夹 -> 打开或者新建一个你想要存代码的文件夹

![image](https://github.com/nobody-x-j/images/blob/main/vscode_open_folder.png)

打开后应该是这样：

![image](https://github.com/nobody-x-j/images/blob/main/vscode_folder_opened.png)

3. 在打开的界面选择 "Terminal" -> "New Terminal" （英文界面） /  “终端” -> “新建终端” (中文界面) 如果看不到 "Terminal" / “终端” ，请把窗口全屏

![image](https://github.com/nobody-x-j/images/blob/main/vscode_new_terminal.png)

打开后应该是这样：

![image](https://github.com/nobody-x-j/images/blob/main/vscode_terminal_opened.png)

4. 在终端输入 git clone https://github.com/nobody-x-j/DGLabMouseListener2.git 从而复制本代码到之前选择的文件夹

```shell
git clone https://github.com/nobody-x-j/DGLabMouseListener2.git
```

![image](https://github.com/nobody-x-j/images/blob/main/vscode_terminal_clone.png)

按回车确认后终端应该会有如下信息，说明你成功将代码存入你的电脑

![image](https://github.com/nobody-x-j/images/blob/main/vscode_terminal_clone_done.png)

5. 在vscode窗口，按"ctrl + shift + p"(三个键同时按)，在跳出的窗口选择 “Python: Select Interpreter” -> 找到刚刚用miniconda3创建的虚拟环境venv -> "Terminal" -> "New Terminal" （英文界面） /  “终端” -> “新建终端” (中文界面) 此时新的终端的命令输入处最左侧出现（venv）则代表成功启动虚拟环境，否则请重启vscode，再 "Terminal" -> "New Terminal" （英文界面） /  “终端” -> “新建终端” (中文界面)， 若还是失败，请试着在miniconda3界面输入code启动vscode

![image](https://github.com/nobody-x-j/images/blob/main/vscode_ctrl_shift_p.png)

![image](https://github.com/nobody-x-j/images/blob/main/vscode_select_interpreter.png)

成功后的终端：

![image](https://github.com/nobody-x-j/images/blob/main/vscode_venv_success.png)

如果反复测试都不成功，尝试在终端输入：

```shell
conda activate venv
```

![image](https://github.com/nobody-x-j/images/blob/main/vscode_venv_manual_activate.png)

如果还不成功，说明之前的步骤操作有误，请删除miniconda3以及vscode，从step 0 重新开始

step 1: 安装以及设置

以下步骤必须确认终端的命令输入处最左侧出现（venv）方可进行

1. 在终端输入 cd DGLabMouseListener2 切换到目标文件夹

```shell
cd DGLabMouseListener2
```

![image](https://github.com/nobody-x-j/images/blob/main/vscode_cd.png)

按下回车后会看到：

![image](https://github.com/nobody-x-j/images/blob/main/vscode_cd_finish.png)

2. 在终端输入 pip install requests websockets loguru pynput 来安装必要的前置程序包 （在DGLabMouseListener2执行过这一步的可以跳过）

```shell
pip install requests websockets loguru pynput
```

![image](https://github.com/nobody-x-j/images/blob/main/vscode_pip_install.png)

成功安装应该是这样的：

![image](https://github.com/nobody-x-j/images/blob/main/vscode_pip_install_success.png)

3. 在vscode界面的最左端（如图）

![image](https://github.com/nobody-x-j/images/blob/main/vscode_config.png)

选中config.py，将ws 里面的内容根据OTC控制器显示的内容自行修改（注：OTC控制器是本程序需要配套的手机app，[点此下载](https://github.com/open-toys-controller/open-DGLAB-controller/releases/latest/download/app-release.apk) [OTC控制器官网](https://github.com/open-toys-controller/open-DGLAB-controller/releases/tag/V1.2.0)）

![image](https://github.com/lxyddice/DGLabMouseListener/assets/95132858/7f1879b3-bc43-4e10-b46d-3b0f3319c23e)

4. 链接设备，开启娱乐模式后，在终端输入 python main.py 即可启动

```shell
python main.py
```

点击鼠标就能看到手机app上显示相应通道有输出了

step 2: 再次开始游戏：

安装之后，再次开始游戏，只需要打开miniconda3，输入 code

```shell
code
```

一般默认打开上次的文件夹，如果没有，请选择打开文件夹，选取程序所在文件夹，打开终端，输入：

```shell
cd DGLabMouseListener2
```

然后输入

```shell
python main.py
```

step 3: 一些自定义选项：

在config.py文件中，有自定义项目，可阅读注释自行修改

在DIY_patterns.py文件中，可以自定义波形，具体格式请参考DIY_patterns.py文件中的注释

需要改变玩法可以自行阅读并修改代码，提示：main.py 42行开始是按键触发相关内容，主要改这里



## 题外话

发现好多人求控但是没人控，就想着让随机数来控制好了喵~

搜了一圈没人写这个玩法，那就我试试吧（） 写的很烂，求教

写的时候其实也开着>_< 被电的很爽（

## 请注意身体，不要玩过头了喵

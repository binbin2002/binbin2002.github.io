---
title: "松灵机器人scout mini小车 自主导航(1)"
date: 2026-03-23
excerpt: "松灵机器人操作."
tags:
- robotics
- navigation
layout: note
---

# 松灵机器人scout mini小车 自主导航

最近实验室来了个松灵机器人scout mini的底座。本着学习的目的对其进行了研究，从最基础的连接开始。

## 1.硬件连接准备

松灵scout mini提供了航空插头用于can串口转USB的操作。
<!-- <div align=center>
<img src="https://img2023.cnblogs.com/blog/3475786/202407/3475786-20240708145520476-1168861472.png" alt="图片名称" >
</div> -->

将通讯航空插头连接到小车对应插口。然后将CAN线引出，将CAN线中的CAN_H和CAN_L分别与CAN_TO_USB适配器相连。然后打开scout mini移动机器人底盘开关，将CAN_TO_USB连接到笔记本的usb口。
具体连接方式如下图所示：

<!-- ![img](https://img2023.cnblogs.com/blog/3475786/202407/3475786-20240708145438573-176386504.png) -->

<font color=Red>注意：一根usb to can线300 money，用的时候要小心保护</font>

## 2.测试硬件与CAN通讯
### 设置CAN_TO_USB对应适配器，检测是否连接成功
1.启动gs_usb 内核模块
```
sudo modprobe gs_usb
```
2.设置500k波特率适配
```
sudo ip link set can0 up type can bitrate 500000  
```
3.如果前面没有出现错误，可以使用命令``ifconfig -a``查看can设备
```
ifconfig -a 
```
4.安装并使用can-utils来测试硬件
```
sudo apt install can-utils
```
5。使用命令监听小车底盘数据
```
candump can0
```
如果前面都没有错，且小车打开状态，执行完``candump can0``后会源源不断收到小车底盘反馈的数据。
如果出现错误，拔插一下重新运行命令。

## 3. ROS功能包测试
松灵机器人提供了对应的ROS功能包用于二次开发。可以通过ROS依赖包直接对小车底盘进行控制。

**3.1.下载ROS相关依赖**
    首先需要根据自己的ROS版本安装对应的依赖，我的是ubuntu18，对应的ROS为melodic
```

#根据自己ROS版本更改命令
sudo apt install ros-melodic-controller-manager
sudo apt install ros-melodic-joint-state-publisher-gui
sudo apt install -y libasio-dev
```
**3.2. 新建工作空间**
新建工作空间，将代码包复制到新建工作空间下的src目录。然后进行编译
```
mkdir -p scout_ws/src
cd scout_ws/src
git clone --recursive https://github.com/agilexrobotics/ugv_sdk.git
git clone https://github.com/agilexrobotics/scout_ros.git
cd ..
catkin_make
```
**3.3 键盘控制小车移动**
在测试完硬件与CAN连接成功后，松灵官方提供了键盘控制小车移动指令
连接电脑usb和小车后，打开电源，运行下面命令：
```
#1)连接设备
sudo ip link set can0 up type can bitrate 500000
#2)测试接受数据
candump can0
#3)运行小车底盘的ros节点 base
cd scout_ws/
source devel/setup.bash
roslaunch scout_bringup scout_mini_robot_base.launch
#4)运行键盘控制节点
source devel/setup.bahs
roslaunch scout_bringup scout_teleop_keyboard.launch
```

<font color=Red>注意：建议先用z将小车速度降低到可控范围内，并打开遥控器确保随时接手控制防止发生碰撞。再运行节点命令</font>
终端的控制界面如下所示：
<!-- ![img](https://img2023.cnblogs.com/blog/3475786/202407/3475786-20240708152710110-1576848414.png) -->
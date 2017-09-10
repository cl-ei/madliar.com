---
layout: post
title: 树莓派之无显示器使用
category: 学习笔记
description: 没有显示器怎么办？别担心，建立远程连接
tags: 编程 树莓派
---

![raspberrypi](/static/blog/img/project/20150629/raspberrypi.jpg)

　　树莓派非常流行的原因之一，就是它在提供了强悍性能的同时还保持着白菜般的价格。官方的指导售价是35美刀，显然这个价格是不包括显示器的。如果你真的要把它当做一台纯粹的电脑来用，那你不免要买键鼠、显示器之类的东西，这个开销就远不止35美元了。为了发挥它最大的价值，下面就来说说抛开显示器，如何来使用树莓派。
<!--more-->
　　步骤是：

　　1、安装树莓派操作系统

　　2、将树莓派接入网络，得知树莓派的IP地址

　　3、通过ssh工具、远程桌面等软件连接树莓派

##安装树莓派系统
　　首先安装系统。在树莓派官网https://www.raspberrypi.org/downloads/ 下载raspbian系统镜像。点击“Download ZIP”，下载完成后解压，得到img镜像。

![raspberrypi](/static/blog/img/project/20150629/raspdownload.jpg)

　　然后在网络上下载“Win32DiskImager”工具，插入内存卡（无需提前格式化），运行Win32DiskImager.exe。如下所示：

![raspberrypi](/static/blog/img/project/20150629/raspimg.jpg)

　　首先选择系统镜像，打开刚才解压的系统镜像，然后在右侧选定插入的内存卡，最后点击“写”，系统会提示此操作将格式化内存卡，点击“确定”，就开始烧录系统了。镜像烧录成功之后，点击安全删除硬件来安全弹出内存卡，即可插入到树莓派上电开机。

　　需要注意的是，安装完系统镜像后，内存卡的可用空间和总空间变为了几十MB，这是正常的现象，因为linux下的分区方式和windows的并不一样。所以，想要往树莓派里传文件的时候，不能直接往内存卡里复制东西，而需要借助U盘等煤质，或者通过网络来传输。

##获取树莓派ip地址
　　将树莓派接入网络是非常简单的，直接连接到路由器的LAN口就行了。如果网络已连接，则网口上的的绿灯将点亮。

　　此时最头疼的问题是，怎么获取树莓派的IP地址呢？因为要远程访问树莓派，ip地址是必知的参数。这里有两个办法.

　　其一，通过串口来访问树莓派。树莓派的开发者可能早就考虑到有相当多的人会不接显示器来使用树莓派，所以树莓派默认就可以通过串口来控制。不过个人不推荐这种方法，因为你需要有一个USB转串口的转换器，如下所示：

![raspberrypi](/static/blog/img/project/20150629/uart.jpg)

　　这个东西十几块钱就可以在淘宝上买到，需要注意的是，有的Usb转串口模块输出的是5V电压，这种转换器和树莓派不兼容，应购买3.3V的。下面把串口转换器和树莓派进行连接。

![raspberrypi](/static/blog/img/project/20150629/gpios.png)

　　在树莓派的GPIO上找到上图对应的三个引脚。（翻转到树莓派背面，第一个GPIO管脚的焊盘是正方形的，找到了第一个引脚的位置，其他对应的引脚也就随之确定）将串口转换器的G与树莓派的Ground引脚相连，然后将串口的TXD连接到树莓派的RXD，再把串口模块的RXD连接到树莓派的TXD。在上电之前需要再三检查，因为新手很有可能因为接线错误导致短路而烧毁整个树莓派。

![raspberrypi](/static/blog/img/project/20150629/connect.jpg)

　　检查无误后，将Usb转串口插入到电脑。从网络上下载SecureCRT软件并安装，单击“File”，选择“Quick Connect”,弹出下面的窗口。

![raspberrypi](/static/blog/img/project/20150629/crtuart1.jpg)

　　选择正确的串口号之后，设置“波特率 115200 无奇偶校验”，开启串口。随便给树莓派发送几个字符，通信正常的话，会收到树莓派的提示：

![raspberrypi](/static/blog/img/project/20150629/uartcon.jpg)

　　这个时候，需要输入用户名和密码来登陆树莓派啦。用户名是“pi”，密码是“raspberry”。进入linux系统之后，输入“ifconfig”，即可看到树莓派的当前地址，这个是内网地址：

![raspberrypi](/static/blog/img/project/20150629/netcon2.jpg)

　　可以看到，ip为192.168.1.102 。

　　第二种获取树莓派ip地址的办法十分简单粗暴，直接登陆路由器的设置页“192.168.1.1”（有的是192.168.0.1），在DHCP服务器栏查看客户端列表，可以看到：

![raspberrypi](/static/blog/img/project/20150629/dhcplist.jpg)

　　其中最后一项客户端名为“raspberry”，地址为192.168.1.102 。（需要注意的是，因为我之前已经将树莓派绑定至静态ip，所以在最后一项有效时间显示为“永久”，如果没有设置，则会显示一个具体的倒计时）

##连接树莓派
　　SSH是一种加密的远程传输协议，可以使用ssh工具来远程访问树莓派。有些linux版本默认是不开启SSH的，但树莓派的开发者可能考虑到很多玩家只有裸机，所以官方系统是开启ssh的，这样给了我们这些没有显示器的玩家极大的方便。这里使用secureCRT软件来连接树莓派。打开secureCRT，单击“File”，选择“Quick Connect”,弹出下面的窗口。

![raspberrypi](/static/blog/img/project/20150629/secureCRT1.jpg)

　　填写树莓派的ip地址与端口号，树莓派ssh连接的端口号默认为22 。单击“connect”，在弹出的“New Host Key”对话框中，选择“accept&save”。然后输入用户名和密码，就可以登陆上树莓派了。

![raspberrypi](/static/blog/img/project/20150629/secureCRT2.jpg)

　　为了让secureCRT更好的显示linux，需要作两项设置：

　　1、设置编码方式UTF-8，以更好兼容中文：Options -> Session Options -> Emulation -> Terminal -> appearance ，在右侧选项框中将Charactor coding由default改为UTF8 。

　　2、设置linux显示格式：Options -> Session Options -> Emulation -> Terminal ->Linux,勾选上ANSI-color。

　　设置完成后，重新连接，就有下面的效果：

![raspberrypi](/static/blog/img/project/20150629/secureCRT3.jpg)

　　这样，就可以通过secureCRT远程来访问树莓派啦！

##使用远程桌面来连接树莓派
　　使用secureCRT只能通过命令行来操作树莓派，因为无法启动x-window所以不能看到图形界面。尽管这样已经足够了，但偶尔还是要用到树莓派的图形界面的，这时候可以使用一款叫VNC的远程桌面软件来连接树莓派。首先需要安装树莓派端的vnc server。

　　secureCRT中输入“sudo apt-get update”更新软件源。然后输入“sudo apt-get install tightvncserver”安装vncserver。安装过程中按y来确定。

　　安装完成后输入“tightvncserver”来启动vnc服务，系统会要求输入密码，再校验一次密码，这个密码是远程桌面的密码。输入两次密码后，会再次询问你是否允许外部控制。如果输入“y”，那么远程桌面就不能控制树莓派，仅仅只是投射树莓派的桌面。所以这里选择“n”，表示允许外部控制。

![raspberrypi](/static/blog/img/project/20150629/vnc1.jpg)

　　注意其中一行：“New "X" desktop is raspberrypi:1 ”，冒号后面所跟的就是通过vnc来访问树莓派的端口，这里是1。在电脑上启动vnc，输入树莓派的ip地址和前面的端口号。

![raspberrypi](/static/blog/img/project/20150629/vnc2.jpg)

　　点击连接，输入刚才输入的密码，即可登录到树莓派桌面。

![raspberrypi](/static/blog/img/project/20150629/vnc3.jpg)

　　树莓派相较于桌面电脑性能低，而且是通过网络来投射的远程桌面，所以使用vnc来访问树莓派给人的感受只有一个字：慢！但其中也有很多有意思的东西，比方说系统自带的几个Python写的小游戏：
![raspberrypi](/static/blog/img/project/20150629/vnc4.jpg)
![raspberrypi](/static/blog/img/project/20150629/vnc5.jpg)
![raspberrypi](/static/blog/img/project/20150629/vnc6.jpg)

　　是不是挺有意思呢？


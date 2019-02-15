# MonitorSystem(堡垒机)
这是一个审计系统，记录所有通过审计系统链接远程机器的用户执行的操作

# 使用技术
* Python 3.6.5
* Django 2.1.1
* sqlite3
* bootstrap
* layui
* shellinabox
* 改写了paramiko
# 项目介绍
  本项目的主要作用是记录运维人员远程操作服务器的操作，做成日志方便查看，在传统的运维和服务器之间多了一个堡垒机(可能还有防火墙)，运维不再直接链接服务器，而是先链接上堡垒机，然后通过堡垒机进行远程链接服务器，这样运维的所有操作都能够通过堡垒机记录下来，方便查找。
  使用了shellinabox实现了网页终端，改写了paramiko，用于记录运维的操作，做成日志
# 项目展示
[![Watch the video](https://raw.github.com/GabLeRoux/WebMole/master/ressources/WebMole_Youtube_Video.png)](https://github.com/Traeric/ProjectSource/blob/master/MonitorSystem/deepin-screen-recorder_Select%20area_20190204110409.mp4)
## 登录页面
![login](https://github.com/Traeric/ProjectSource/blob/master/MonitorSystem/photo/1.png)
## 主页
![dashboard](https://github.com/Traeric/ProjectSource/blob/master/MonitorSystem/photo/2.png)
## SSH链接
![ssh](https://github.com/Traeric/ProjectSource/blob/master/MonitorSystem/photo/3.png)
## 日志记录
![log](https://github.com/Traeric/ProjectSource/blob/master/MonitorSystem/photo/4.png)
## 日志详细
![log_detail](https://github.com/Traeric/ProjectSource/blob/master/MonitorSystem/photo/5.png)
## 日志查询
![log_search](https://github.com/Traeric/ProjectSource/blob/master/MonitorSystem/photo/6.png)
## 批量命令
![batch_command](https://github.com/Traeric/ProjectSource/blob/master/MonitorSystem/photo/7.png)
## 文件上传
![file_upload](https://github.com/Traeric/ProjectSource/blob/master/MonitorSystem/photo/8.png)
## 文件下载
![file_download](https://github.com/Traeric/ProjectSource/blob/master/MonitorSystem/photo/9.png)
## 设置页面
![settings](https://github.com/Traeric/ProjectSource/blob/master/MonitorSystem/photo/10.png)

大致页面如此，还有一些页面不做赘述

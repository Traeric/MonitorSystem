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
## 登录页面
![login]("https://pan.baidu.com/s/1qEa4qc4BrDYhLl8q7R1BKA#list/path=%2Fgithub%E8%BF%9C%E7%A8%8B%E8%B5%84%E6%BA%90%2FMonitorSystem%2Fphoto")



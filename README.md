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
![login](https://thumbnail0.baidupcs.com/thumbnail/9017b8d67e7e25774119ba61a58cab35?fid=776928879-250528-809600106491195&time=1549252800&rt=sh&sign=FDTAER-DCb740ccc5511e5e8fedcff06b081203-TBtVAjOSw604WQWzlZlSu9q5g74%3D&expires=8h&chkv=0&chkbd=0&chkpc=&dp-logid=800349333684327134&dp-callid=0&size=c1920_u1080&quality=90&vuk=-&ft=video&autopolicy=1)



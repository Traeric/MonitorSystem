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
[![Watch the video](https://raw.github.com/GabLeRoux/WebMole/master/ressources/WebMole_Youtube_Video.png)](https://pan.baidu.com/s/1qEa4qc4BrDYhLl8q7R1BKA?fid=115385112122917)
## 登录页面
![login](https://thumbnail0.baidupcs.com/thumbnail/9017b8d67e7e25774119ba61a58cab35?fid=776928879-250528-809600106491195&time=1549252800&rt=sh&sign=FDTAER-DCb740ccc5511e5e8fedcff06b081203-TBtVAjOSw604WQWzlZlSu9q5g74%3D&expires=8h&chkv=0&chkbd=0&chkpc=&dp-logid=800349333684327134&dp-callid=0&size=c1920_u1080&quality=90&vuk=-&ft=video&autopolicy=1)
## 主页
![dashboard](https://thumbnail0.baidupcs.com/thumbnail/41c51676a47c502a27519ce50cf99f62?fid=776928879-250528-321800611156352&time=1549252800&rt=sh&sign=FDTAER-DCb740ccc5511e5e8fedcff06b081203-DCr4HJjsQIih2EtnZsiRQquGiyg%3D&expires=8h&chkv=0&chkbd=0&chkpc=&dp-logid=800349333684327134&dp-callid=0&size=c1920_u1080&quality=90&vuk=-&ft=video&autopolicy=1)
## SSH链接
![ssh](https://thumbnail0.baidupcs.com/thumbnail/2e931551dad6b6fba8db6cbcb477cde1?fid=776928879-250528-950479771975979&time=1549252800&rt=sh&sign=FDTAER-DCb740ccc5511e5e8fedcff06b081203-5%2FlM2l3iRtXQ7CP3tFY8HvSLhpQ%3D&expires=8h&chkv=0&chkbd=0&chkpc=&dp-logid=800349333684327134&dp-callid=0&size=c1920_u1080&quality=90&vuk=-&ft=video&autopolicy=1)
## 日志记录
![log](https://thumbnail0.baidupcs.com/thumbnail/5352692ed8074056f02bb493f9cb1f83?fid=776928879-250528-667668445748449&time=1549252800&rt=sh&sign=FDTAER-DCb740ccc5511e5e8fedcff06b081203-9SCfZhvI672D%2BEUb5mqOzyMR%2BX8%3D&expires=8h&chkv=0&chkbd=0&chkpc=&dp-logid=800349333684327134&dp-callid=0&size=c1920_u1080&quality=90&vuk=-&ft=video&autopolicy=1)
## 日志详细
![log_detail](https://thumbnail0.baidupcs.com/thumbnail/7e9c6f70fa98dd9484225f017dd5a07b?fid=776928879-250528-505734306459080&time=1549252800&rt=sh&sign=FDTAER-DCb740ccc5511e5e8fedcff06b081203-Tjh0uIGGlCRwTOTvzp2iTlxdu60%3D&expires=8h&chkv=0&chkbd=0&chkpc=&dp-logid=800349333684327134&dp-callid=0&size=c1920_u1080&quality=90&vuk=-&ft=video&autopolicy=1)
## 日志查询
![log_search](https://thumbnail0.baidupcs.com/thumbnail/f4d8cf8e4922a4e08ea64cb4d3024d07?fid=776928879-250528-851594139906737&time=1549252800&rt=sh&sign=FDTAER-DCb740ccc5511e5e8fedcff06b081203-1HbpVgBEuzm7j1IIpKeNGBqjOQU%3D&expires=8h&chkv=0&chkbd=0&chkpc=&dp-logid=800349333684327134&dp-callid=0&size=c1920_u1080&quality=90&vuk=-&ft=video&autopolicy=1)
## 批量命令
![batch_command](https://thumbnail0.baidupcs.com/thumbnail/d1d2408db15f87d58699133fbd19f913?fid=776928879-250528-841250612912571&time=1549252800&rt=sh&sign=FDTAER-DCb740ccc5511e5e8fedcff06b081203-Lk%2Byk26z8fTizb8WTdrlK0fCu74%3D&expires=8h&chkv=0&chkbd=0&chkpc=&dp-logid=800349333684327134&dp-callid=0&size=c1920_u1080&quality=90&vuk=-&ft=video&autopolicy=1)
## 文件上传
![file_upload](https://thumbnail0.baidupcs.com/thumbnail/cdb00057ea0a4408f7ceb0c6d99ff913?fid=776928879-250528-144022367015091&time=1549252800&rt=sh&sign=FDTAER-DCb740ccc5511e5e8fedcff06b081203-7mf9qVSs1SMxrFtV8mM7lNHGudE%3D&expires=8h&chkv=0&chkbd=0&chkpc=&dp-logid=800349333684327134&dp-callid=0&size=c1920_u1080&quality=90&vuk=-&ft=video&autopolicy=1)
## 文件下载
![file_download](https://thumbnail0.baidupcs.com/thumbnail/462fcff1904a2bfeda32bbed4f8a9758?fid=776928879-250528-768369938822166&time=1549252800&rt=sh&sign=FDTAER-DCb740ccc5511e5e8fedcff06b081203-nHq6UjPCz7rT7yS4PLA844Q8YcU%3D&expires=8h&chkv=0&chkbd=0&chkpc=&dp-logid=800349333684327134&dp-callid=0&size=c1920_u1080&quality=90&vuk=-&ft=video&autopolicy=1)
## 设置页面
![settings](https://thumbnail0.baidupcs.com/thumbnail/d91dea9784c8aaa179fb60b483fc8927?fid=776928879-250528-305397075846627&time=1549252800&rt=sh&sign=FDTAER-DCb740ccc5511e5e8fedcff06b081203-6TEUU%2BUKUz9Fvhmdn2QtT%2FAJDpI%3D&expires=8h&chkv=0&chkbd=0&chkpc=&dp-logid=800349333684327134&dp-callid=0&size=c1920_u1080&quality=90&vuk=-&ft=video&autopolicy=1)

大致页面如此，还有一些页面不做赘述

from django.test import TestCase

# Create your tests here.

import paramiko

# # 模拟一个ssh的客户端
# ssh = paramiko.SSHClient()
# # 相当于在ssh连接的时候将秘钥写入known_hosts，相当于ssh连接的时候输入yes
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# # 连接
# ssh.connect('172.16.91.131', 22, 'ericjin', '0528')
# # 执行命令返回3个结果，标准输入，输出和错误
# stdin, stdout, stderr = ssh.exec_command('ip addr')
# # 打印标准输出
# print(stdout.read().decode())
# # 关闭连接
# ssh.close()


import datetime

# date = datetime.datetime.strptime("2017-8-27", "%Y-%m-%d")
# print(date)
# print(int("02"))

# if not "":
#     print("============")


status_choices = (
    (0, "initialized"),
    (1, "sucess"),
    (2, "failed"),
    (3, "timeout"),
)
# print(list(map(lambda x: x[1], status_choices)))

a = [1, 2, 5]
print()



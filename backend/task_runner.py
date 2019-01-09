import os
import sys

import paramiko
import django
from concurrent.futures import ProcessPoolExecutor


def ssh_connect(task_detail_log):
    host_to_remote_user = task_detail_log.host_to_remote_users
    # 模拟一个ssh的客户端
    ssh = paramiko.SSHClient()
    # 相当于在ssh连接的时候将秘钥写入known_hosts，相当于ssh连接的时候输入yes
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接
    try:
        ssh.connect(
            hostname=host_to_remote_user.host.ip_addr,
            port=host_to_remote_user.host.port,
            username=host_to_remote_user.remote_user.username,
            password=host_to_remote_user.remote_user.password,
            timeout=5                       # 配置超时时间为5秒
        )
        # 执行命令返回3个结果，标准输入，输出和错误
        stdin, stdout, stderr = ssh.exec_command(task_detail_log.task.content)
        # 获取结果
        stdout_res = stdout.read().decode()
        stderr_res = stderr.read().decode()
        # 获取详细的主机命令执行信息
        task_detail_log.result = stdout_res + stderr_res
        if stderr_res:
            task_detail_log.status = 2
        else:
            task_detail_log.status = 1
    except Exception as e:
        task_detail_log.result = e
        task_detail_log.status = 2
    task_detail_log.save()
    # 关闭连接
    ssh.close()


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(base_dir)
    # 设置系统的环境变量
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CrazyEye.settings")
    # 让脚本可以操作Django数据库
    django.setup()

    from monitor import models
    if len(sys.argv) == 1:
        exit("task id not provided!")
    task_id = sys.argv[1]
    task_obj = models.Task.objects.get(id=task_id)
    print("task runner...", task_id)
    # 起一个进程池
    pool = ProcessPoolExecutor(10)
    for task_detail_obj in task_obj.tasklogdetail_set.select_related():
        pool.submit(ssh_connect, task_detail_obj)
    pool.shutdown(wait=True)

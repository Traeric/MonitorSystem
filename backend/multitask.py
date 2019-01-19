import os
import subprocess
from django import conf


class MultiTask(object):
    """执行批量命令"""
    def __init__(self, request, models):
        self.request = request
        self.models = models
        self.task_id = None
        self.call()

    def call(self):
        """
        执行task
        :return:
        """
        request = self.request
        # 获取主机列表
        host_to_remote_user_ids = request.POST.getlist('host-to-remote-user-ids')
        batch_type = request.POST.get("batch-type", None)
        if hasattr(self, batch_type):
            func = getattr(self, batch_type)
            # 执行批量方法
            func(host_to_remote_user_ids)

    def cmd(self, host_ids):
        """
        批量命令执行
        :param host_ids:
        :return:
        """
        request = self.request
        command = request.POST.get('command', None)
        self.public(command, host_ids)

    def file_upload(self, host_ids):
        """
        本地文件上传
        :param host_ids:
        :return:
        """
        request = self.request
        # 获取参数
        upload_path = request.POST.get("file_path", None)   # 堡垒机文件上传位置
        remote_path = request.POST.get("remote_path", None)  # 远程主机位置
        self.public(content="传送本地文件到远程", host_ids=host_ids,
                    task_type="file_upload", params=[upload_path, remote_path])

    def file_download(self, host_ids):
        """
        远程文件下载
        :param host_ids:
        :return:
        """
        request = self.request
        # 获取参数
        remote_path = request.POST.get("remote_path", None)
        self.public(content="从远程下载文件", host_ids=host_ids,
                    task_type="file_download", params=["zw", remote_path])

    def public(self, content, host_ids, task_type="cmd", params=None):
        """
        批量命令共同执行的方法
        :param content:
        :param host_ids:
        :param task_type:
        :param params:
        :return:
        """
        # 创建一条Task记录
        task_obj = self.models.Task.objects.create(
            task_type=task_type,
            content=content,
            user=self.request.user
        )
        # 创建该条记录下的TaskLogDetail记录
        task_log_details = []
        for host_id in set(host_ids):
            task_log_obj = self.models.TaskLogDetail(
                task=task_obj,
                host_to_remote_users_id=host_id,
                result="init...",
            )
            task_log_details.append(task_log_obj)
        # 批量创建
        self.models.TaskLogDetail.objects.bulk_create(task_log_details)
        # 脱离Django执行脚本
        path = os.path.join(conf.settings.BASE_DIR, "backend", "task_runner.py")
        if task_type == "cmd":
            task_script = "python3 {0} {1} {2}".format(path, task_obj.id, task_type)
        else:
            task_script = "python3 {0} {1} {2} {3} {4}".format(path, task_obj.id, task_type, params[0], params[1])
        subprocess.Popen(task_script, shell=True)
        self.task_id = task_obj.id


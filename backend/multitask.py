import os
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
        request = self.request
        command = request.POST.get('command', None)
        # 创建一条Task记录
        task_obj = self.models.Task.objects.create(
            content=command,
            user=request.user
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
        import subprocess
        path = os.path.join(conf.settings.BASE_DIR, "backend", "task_runner.py")
        task_script = "python3 {0} {1}".format(path, task_obj.id)
        subprocess.Popen(task_script, shell=True)
        self.task_id = task_obj.id



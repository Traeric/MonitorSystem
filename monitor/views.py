import json
import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, HttpResponse
from django import conf
from django.contrib.auth import logout
from . import models
from backend.multitask import MultiTask
from dwebsocket.decorators import accept_websocket

# Create your views here.
from django.views import View


class WebSSH(LoginRequiredMixin, View):
    """web上连接ssh"""

    def get(self, request):
        # 获取堡垒机的ip跟端口
        ip = conf.settings.CRAZYEYE_IP
        port = conf.settings.CRAZYEYE_PORT
        return render(request, "web_ssh.html", locals())


class LogPage(LoginRequiredMixin, View):
    """审计日志"""

    def get(self, request):
        # 获取所有的主机
        hosts = models.Host.objects.select_related()
        return render(request, "log/log_page.html", locals())


class LockScreem(View):
    """锁屏"""

    def get(self, request):
        # 获取用户登录邮箱
        email = request.COOKIES.get("email", None)
        return render(request, "login/lock_screen.html", {'email': email})

    def post(self, request):
        email = request.user.email
        # 退出登录
        logout(request)
        return HttpResponse(email)


class HostLog(LoginRequiredMixin, View):
    """主机日志"""

    def get(self, request, host_id):
        # 获取主机信息
        host = models.Host.objects.get(id=host_id)
        # 查询出与该主机相关的所有账户
        host_to_remote_users = host.hosttoremoteuser_set.select_related()
        # 查询与该主机相关的所有日志信息
        logs = []
        for item in host_to_remote_users:
            for log in item.auditlog_set.all():
                logs.append(log)
        return render(request, "log/host_log.html", locals())


class LogFilter(LoginRequiredMixin, View):
    """日志筛选"""

    def get(self, request):
        # 获取参数
        filter_type = request.GET.get("filter_type")
        search_field = request.GET.get("search_field")
        start_time = request.GET.get("start_time", None)
        end_time = request.GET.get("end_time", None)
        q_filter = Q()
        q_filter.connector = 'AND'
        # 确定筛选的时间
        if start_time and not end_time:
            q_filter.children.append(("record_date__gte", start_time))
        elif start_time and end_time:
            q_filter.children.append(("record_date__gte", start_time))
            q_filter.children.append(("record_date__lte", end_time))
        elif not start_time and end_time:
            q_filter.children.append(("record_date__lte", end_time))
        if filter_type == 'user':
            # 按照用户名筛选
            q_filter.children.append(("crazy_eye_account__name", search_field))
        elif filter_type == 'host':
            # 按照主机名筛选
            q_filter.children.append(("host_to_remote_users__host__name", search_field))
        log_obj = models.AuditLog.objects.filter(q_filter)
        return render(request, "log/log_filter.html", locals())


class BatchCmd(LoginRequiredMixin, View):
    """批量命令操作"""

    def get(self, request):
        # 拿到该用户下所有的主机组
        host_groups = request.user.host_group.all()
        none_group = request.user.host_to_remote_users.all()
        # 拿到最近执行的批量任务
        batch_command = models.Task.objects.filter(user=request.user, task_type="cmd").order_by("-id").all()
        batch_command = batch_command if len(batch_command) < 10 else batch_command[:10]
        return render(request, 'host_manage/batch_cmd.html', locals())

    def post(self, request):
        # 获取参数
        task_obj = MultiTask(request, models)
        result = list(models.Task.objects.filter(id=task_obj.task_id).values(
            "id",
            "tasklogdetail__host_to_remote_users__host__name",
            "tasklogdetail__host_to_remote_users__host__ip_addr",
            "tasklogdetail__host_to_remote_users__host__os_type",
            "tasklogdetail__host_to_remote_users__remote_user__username",
            "tasklogdetail__status",
        ))
        result.append(list(map(lambda x: x[1], models.TaskLogDetail.status_choices)))
        import json
        return HttpResponse(json.dumps(result))


class BatchFile(LoginRequiredMixin, View):
    """批量操作文件"""

    def get(self, request):
        # 拿到该用户下所有的主机组
        host_groups = request.user.host_group.all()
        none_group = request.user.host_to_remote_users.all()
        # 拿到最近执行的批量任务
        batch_command = models.Task.objects.filter(user=request.user).exclude(task_type="cmd").order_by("-id").all()
        batch_command = batch_command if len(batch_command) < 10 else batch_command[:10]
        return render(request, "host_manage/batch_file.html", locals())


@accept_websocket
def host_detail_info(request):
    """
    websocket链接实时获取主机执行命令的状态
    :param request:
    :return:
    """
    websocket = request.websocket
    for message in websocket:
        # 获取任务id
        task_id = int(message)
        # 定时获取主机信息
        send_id = []    # 已经推送的主机id
        while True:
            task_obj = models.Task.objects.filter(id=task_id)
            task_detail_objs = task_obj[0].tasklogdetail_set.select_related()
            for task_detail_obj in task_detail_objs:
                if task_detail_obj.status != 0:
                    # 如果不是准备状态，表示已经获取到结果
                    if task_detail_obj.id not in send_id:
                        # 将消息推送到客户端
                        send_id.append(task_detail_obj.id)
                        import json
                        websocket.send(json.dumps(
                            [
                                task_detail_obj.host_to_remote_users.host.name,
                                task_detail_obj.host_to_remote_users.remote_user.username,
                                task_detail_obj.result,
                                task_detail_obj.status,
                            ]
                        ))
            if len(send_id) == task_detail_objs.count():
                break
            time.sleep(2)
        time.sleep(2)
        return


class FileTransfer(LoginRequiredMixin, View):
    """批量文件操作"""

    def post(self, request):
        file = request.FILES.get("file")
        base_dir = conf.settings.BATCH_FILE_DIR
        import os
        ret_msg = {
            "status_code": 200,
            "info": "file upload success",
        }
        try:
            import time
            file_split = file.name.rsplit(".", 1)
            file_path = os.path.join(base_dir, "upload", "%s%s.%s" % (file_split[0], time.time(), file_split[1]))
            with open(file_path, r'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            ret_msg['file_path'] = file_path
            return HttpResponse(json.dumps(ret_msg))
        except Exception as e:
            ret_msg['status_code'] = 500   # 写入失败
            ret_msg['info'] = "file upload error, error msg is %s" % e
            return HttpResponse(json.dumps(ret_msg))


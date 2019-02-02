import hashlib
import json
import os
import time

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http.response import FileResponse
from django.shortcuts import render, HttpResponse, redirect
from django import conf
from django.contrib.auth import logout
from django.urls import reverse

from . import models
from backend.multitask import MultiTask
from dwebsocket.decorators import accept_websocket
from django.conf import settings

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

    def post(self, request, host_id):
        """
        日志记录查询，按堡垒机用户，远程主机用户以及筛选日志类型
        :param request:
        :param host_id:
        :return:
        """
        # 获取主机信息
        host = models.Host.objects.get(id=host_id)
        host_to_remote_users = None
        # 获取搜索的type
        search_type = request.POST.get("type", None)
        if search_type == "search":
            # input搜索
            # 获取搜索的内容
            value = request.POST.get("value", None)
            content = request.POST.get("search_field", None)
            if value == "user":
                # 搜索相应的堡垒机用户
                # 查询出与该主机相关的所有账户
                host_to_remote_users = host.hosttoremoteuser_set.filter(userprofile__name=content)
            elif value == "remote":
                # 根据远程主机的用户名搜索日志
                # 查询符合条件的远程用户
                host_to_remote_users = host.hosttoremoteuser_set.filter(remote_user__username=content)
        # 获取要查询的日志
        logs = []
        if search_type == "type":
            host_to_remote_users = host.hosttoremoteuser_set.select_related()
        for items in host_to_remote_users:
            if search_type == "type":
                value = request.POST.get("value", None)
                log_type = {
                    "login": 0,
                    "cmd": 1,
                    "logout": 2,
                }
                for log in items.auditlog_set.filter(log_type=log_type[value]):
                    logs.append(log)
            else:
                for log in items.auditlog_set.all():
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
        send_id = []  # 已经推送的主机id
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

    def get(self, request):
        """
        下载文件到本地
        :param request:
        :return:
        """
        # 获取文件路径
        file_path = request.GET.get("file", None)
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s"' % file_path.rsplit("/", maxsplit=1)[1]
        return response

    def post(self, request):
        """
        上传文件
        :param request:
        :return:
        """
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
            ret_msg['status_code'] = 500  # 写入失败
            ret_msg['info'] = "file upload error, error msg is %s" % e
            return HttpResponse(json.dumps(ret_msg))


@login_required
def cmd_display(request, cmd_id):
    """
    查询批量命令的详细结果
    :param request:
    :param cmd_id:
    :return:
    """
    # 查询数主Task
    task_obj = models.Task.objects.filter(id=cmd_id)
    # 查询出主Task下的task detail
    task_detals = task_obj[0].tasklogdetail_set.select_related()
    cmd_list = []  # 传到前端的记录
    for task_detal in task_detals:
        # 获取单条记录的信息
        detail_obj = {
            'result': task_detal.result,
            'status': task_detal.status,
            'date': str(task_detal.date),
            'host': task_detal.host_to_remote_users.host.name,
            'ip_addr': task_detal.host_to_remote_users.host.ip_addr,
        }
        cmd_list.append(detail_obj)
    return HttpResponse(json.dumps({
        "cmd_list": cmd_list,
        "task_type": task_obj[0].task_type,
        'content': task_obj[0].content,
        'user': task_obj[0].user.name,
        'email': task_obj[0].user.email,
    }))


class SettingHome(LoginRequiredMixin, View):
    """设置页面"""

    def get(self, request):
        user = request.user
        # 查询与该用户相关的所有的主机以及远程账户
        remote_users = list(user.host_to_remote_users.all())
        hosts = set(map(lambda x: x.host, remote_users))
        return render(request, "settings/set_home.html", locals())

    def delete(self, request):
        host_to_remote_user_id = int(request.body.decode().split("=")[1])
        # 移除指定的远程用户关系
        try:
            request.user.host_to_remote_users.remove(host_to_remote_user_id)
            return HttpResponse(json.dumps({
                "flag": True,
                "message": "移除成功"
            }))
        except Exception:
            return HttpResponse(json.dumps({
                "flag": False,
                "message": "移除失败"
            }))


class Authentication(LoginRequiredMixin, View):
    """修改邮箱跟密码"""

    def get(self, request):
        """
        处理邮箱认证链接
        :param request:
        :return:
        """
        # 获取参数
        email = request.GET.get("email", None)
        token = request.GET.get("token", None)
        # 获取key跟时间
        auth_key, ctime = token.split("|")
        auth_time = float(ctime)
        # 进行md5加密
        auth_str = "%s|%f" % (settings.SECRET_KEY, auth_time)
        md5 = hashlib.md5()
        md5.update(bytes(auth_str, encoding="utf-8"))
        md5_key = md5.hexdigest()
        # 进行是否超时验证
        if (time.time() - (100 * 60)) > auth_time:
            msg = "Sorry!!  Verify timeout..."
            return render(request, "error_page/error.html", locals())
        # 验证秘钥是否正确
        if not md5_key == auth_key:
            msg = "Authenticate key is error..."
            return render(request, "error_page/error.html", locals())
        # 验证通过，修改邮箱
        user = request.user
        user.email = email
        user.save()
        # 修改成功
        path = reverse("setting_home")
        return redirect(to=path)

    def post(self, request):
        """
        获取要修改的邮箱并发送信息给用户
        :param request:
        :return:
        """
        # 获取新的邮箱
        new_email = request.POST.get("new_email", None)
        # 给新邮箱发送验证消息
        subject = "堡垒机修改邮箱"
        email_from = settings.DEFAULT_FROM_EMAIL
        # 生成链接
        name = request.user.name
        current_time = time.time()  # 获取当前时间
        token_with_time = "%s|%f" % (settings.SECRET_KEY, current_time)  # 拼接字符串
        # md5加密
        md5 = hashlib.md5()
        md5.update(bytes(token_with_time, encoding="utf-8"))
        auth_key = md5.hexdigest()  # 获取加密后的值
        # 将加密后的字符串与当前时间一起发过去
        token = "%s|%f" % (auth_key, current_time)
        # 生成链接
        path = "http://127.0.0.1:8000/monitor/email_modify"
        link = "{0}?email={1}&token={2}".format(path, new_email, token)
        try:
            filepath = os.path.join(settings.BASE_DIR, 'templates', 'settings', 'send_email.html')
            with open(filepath, "r", encoding="utf8") as f:
                html_content = f.read()
            # 替换内容
            html_content = html_content.replace("{zw name zw}", name).replace("{zw link zw}", link)
            # 生成msg
            msg = EmailMultiAlternatives(subject, html_content, email_from, [new_email])
            msg.attach_alternative(html_content, "text/html")
            # 发送邮件
            msg.send()
            return HttpResponse(json.dumps({
                "status": True,
                "message": "发送成功，请尽快登录邮箱进行验证，有效时间为15分钟。",
            }))
        except Exception:
            # 发送出错
            return HttpResponse(json.dumps({
                "status": False,
                "message": "发送失败，请重试。",
            }))


@login_required
def username_modify(request):
    """
    用户名修改
    :param request:
    :return:
    """
    # 获取用户名
    if request.method == "POST":
        username = request.POST.get("username", None)
        if username != "":
            # 修改用户名
            request.user.name = username
            try:
                request.user.save()
                return HttpResponse(json.dumps({
                    "status": True,
                    "message": "用户名修改成功",
                }))
            except Exception:
                return HttpResponse(json.dumps({
                    "status": False,
                    "message": "用户名修改失败",
                }))


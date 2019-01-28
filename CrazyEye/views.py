from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from monitor import models


@login_required
def dashboard(request):
    """
    主页
    :param request:
    :return:
    """
    # 查询最近的十条批量操作记录
    task_obj = models.Task.objects.order_by("-id")[:10]
    # 获取注册用户数
    user_number = models.UserProfile.objects.count()
    # 已经管理的服务器
    host_count = models.Host.objects.count()
    # 查询最近登录的用户
    return render(request, "dashboard.html", locals())


def log_in(request):
    """
    用户登录
    :param request:
    :return:
    """
    error_message = ""
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        login_type = request.POST.get("login_type", None)
        # 进行验证
        user = authenticate(username=username, password=password)
        if user:
            # 验证成功，登录
            login(request, user)
            # 修改登录时间
            import datetime
            request.user.last_login = datetime.datetime.now()
            return redirect(request.GET.get("next", "/"))
        else:
            # 登录失败
            error_message = "You have a wrong user name or password!"
            if login_type is not None:
                # 是在锁屏页面
                return HttpResponse("You have a wrong password!")
    return render(request, "login/login.html", {"error_message": error_message})


def log_out(request):
    """
    登出
    :param request:
    :return:
    """
    logout(request)
    return redirect("/login")

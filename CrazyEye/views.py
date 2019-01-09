from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout


@login_required
def dashboard(request):
    """
    主页
    :param request:
    :return:
    """
    return render(request, "dashboard.html")


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

"""CrazyEye URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^lock_screem/$', views.LockScreem.as_view(), name="lock_screem"),
    url(r'^web_ssh/$', views.WebSSH.as_view(), name="web_ssh"),
    url(r'^log_page.html/$', views.LogPage.as_view(), name="log_page"),
    url(r'^host_log_detail/(?P<host_id>\d+)/$', views.HostLog.as_view(), name="host_log"),
    url(r'^log_filter/$', views.LogFilter.as_view(), name="log_filter"),
    url(r'^batch_cmd/$', views.BatchCmd.as_view(), name='batch_cmd'),
    url(r'^batch_file/$', views.BatchFile.as_view(), name='batch_file'),
    # websocket获取主机执行命令的信息
    url(r'^host_detail_info/$', views.host_detail_info),
]

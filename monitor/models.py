from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


# Create your models here.


class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=64, verbose_name="用户名", unique=True)
    host_to_remote_users = models.ManyToManyField(to="HostToRemoteUser", verbose_name="关联主机账户")
    host_group = models.ManyToManyField(to="HostGroup", verbose_name="主机组")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'  # 使用email作为用户名
    REQUIRED_FIELDS = ['name']  # 必须要有的字段

    def __str__(self):
        return self.email


class IDC(models.Model):
    """IDC机房"""
    name = models.CharField(max_length=64, verbose_name="IDC机房名")

    def __str__(self):
        return self.name


class Host(models.Model):
    """存储主机列表"""
    name = models.CharField(max_length=64, unique=True, verbose_name="主机名")
    ip_addr = models.CharField(max_length=64, unique=True, verbose_name="ip地址")
    port = models.IntegerField(default=22, verbose_name="端口号")
    idc = models.ForeignKey(to=IDC, on_delete=models.CASCADE)
    os_type = models.CharField(max_length=64, verbose_name="系统类型", null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="主机注册时间")

    def __str__(self):
        return self.name


class HostGroup(models.Model):
    """存储主机组"""
    name = models.CharField(max_length=64, unique=True, verbose_name="组名")
    host_to_remote_users = models.ManyToManyField(to="HostToRemoteUser")
    date = models.DateTimeField(auto_now_add=True, verbose_name="主机组注册时间")

    def __str__(self):
        return self.name


class HostToRemoteUser(models.Model):
    """主机跟RemoteUser多对多关联的第三张表"""
    host = models.ForeignKey(to=Host, on_delete=models.CASCADE)
    remote_user = models.ForeignKey(to="RemoteUser", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("host", "remote_user")

    def __str__(self):
        return "%s - %s" % (self.host, self.remote_user)


class RemoteUser(models.Model):
    """存储远程要管理的主机的账号信息"""
    username = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(max_length=64, verbose_name="密码")
    auth_type_choice = (
        (0, "ssh-password"),
        (1, "ssh-key")
    )
    auth_type = models.SmallIntegerField(choices=auth_type_choice, verbose_name="认证方式")

    class Meta:
        unique_together = (("username", "password", "auth_type"),)

    def __str__(self):
        return self.username


class AuditLog(models.Model):
    """存储审计日志"""
    crazy_eye_account = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, verbose_name="堡垒机账号")
    host_to_remote_users = models.ForeignKey(to=HostToRemoteUser, on_delete=models.CASCADE)
    log_type_choice = (
        (0, "login"),
        (1, "cmd"),
        (2, "logout"),
    )
    log_type = models.SmallIntegerField(choices=log_type_choice, default=1, verbose_name="日志类型")
    content = models.CharField(max_length=255, verbose_name="日志内容")
    record_date = models.DateTimeField(auto_now_add=True, verbose_name="记录日期")

    def __str__(self):
        return "%s - %s - %s" % (self.host_to_remote_users, self.content, self.record_date)


class Task(models.Model):
    """批量任务"""
    task_type_choice = (
        ('cmd', '批量命令'),
        ('file_upload', "传送本地文件到远程"),
        ('file_download', "从远程下载文件"),
    )
    task_type = models.CharField(max_length=16, choices=task_type_choice, default="cmd")
    content = models.CharField(max_length=255, verbose_name="任务内容")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.task_type, self.content)


class TaskLogDetail(models.Model):
    """存储大任务的子结果"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    host_to_remote_users = models.ForeignKey(HostToRemoteUser, on_delete=models.CASCADE)
    result = models.TextField(verbose_name="任务执行结果")
    status_choices = (
        (0, "initialized"),
        (1, "sucess"),
        (2, "failed"),
        (3, "timeout"),
    )
    status = models.SmallIntegerField(choices=status_choices, default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.task, self.host_to_remote_users)





from django.contrib.auth import authenticate
from . import paramiko_connect
from monitor import models
import getpass


class SSHInteractive(object):
    """启动堡垒机交互脚本"""

    def __init__(self, argv_handler_instance):
        self.argv_handler_instance = argv_handler_instance
        self.models = models
        self.user = None

    def auth(self):
        """
        登录认证
        :return:
        """
        # 允许错误3次
        count = 0
        while count < 3:
            username = input("请输入堡垒机账号：").strip()
            password = getpass.getpass("Password:").strip()
            # 验证
            user = authenticate(username=username, password=password)
            if user:
                # 认证成功
                self.user = user
                return True
            else:
                if count < 2:
                    print("you have a username or password wrong, please re-input and you still have %d chance..." %
                          (2 - count))
                count += 1
        else:
            print("you have a max wrong count...")
            return False

    def interactive(self):
        """
        启动交互脚本
        :return:
        """
        # 登录认证
        if self.auth():
            # 认证成功，打印所有授权给这个用户的主机信息
            print("Ready to print all the authorized hosts...to this user...")
            # 输出所有的该账户关联的主机组
            host_groups = self.user.host_group.all()
            while True:
                print("index\tGroup Name\tHost Number")
                for index, host_group in enumerate(host_groups):
                    print_str = ("{index}\t {group_name}\t\t {count}"
                                 .format(index=index,
                                         group_name=host_group.name,
                                         count=host_group.host_to_remote_users.count()))
                    print(print_str)
                print("z\t 未分组主机\t %s" % self.user.host_to_remote_users.count())
                choice = input("请选择要查看的主机组，按q退出>>>: ").strip()
                global selected_host_group
                if choice.isdigit():
                    choice = int(choice)
                    # 拿到用户选择的主机
                    selected_host_group = host_groups[choice]
                elif choice == "z":
                    selected_host_group = self.user
                elif choice == "q":
                    break
                while True:
                    # 拿到该主机组下所有主机
                    host_to_remote_users = selected_host_group.host_to_remote_users.all()
                    print("----" * 8)
                    print("index\thost")
                    for index, host_to_remote_user in enumerate(host_to_remote_users):
                        print("%s\t%s" % (index, host_to_remote_user))
                    choice = input("请选择主机，按b返回>>>: ").strip()
                    if choice.isdigit():
                        choice = int(choice)
                        selected_host = host_to_remote_users[choice]
                        print("going to login %s with %s..." % (selected_host.host, selected_host.remote_user))
                        # 开始连接
                        paramiko_connect.ssh_connect(self, selected_host)
                    elif choice == "b":
                        break

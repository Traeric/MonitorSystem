from . import ssh_interactive


class ArgvHandler(object):
    """接收用户参数，并调用相应的功能"""

    def __init__(self, sys_args):
        self.sys_args = sys_args

    @staticmethod
    def help_msg(error_msg=""):
        """
        打印帮助信息，说明有哪些功能
        :param error_msg:
        :return:
        """
        msg = """
        {error_msg}
        run    启动用户交互程序
        """.format(error_msg=error_msg)
        exit(msg)

    def run(self):
        """
        启动用户交互程序
        :return:
        """
        obj = ssh_interactive.SSHInteractive(self)
        obj.interactive()

    def call(self):
        """
        根据用户输入的参数，调用相应的功能
        :return:
        """
        if len(self.sys_args) == 1:
            # 等于1，代表什么也没有输入，包含脚本sys_args里面第0位是脚本本身
            self.help_msg()
        if hasattr(self, self.sys_args[1]):
            # 获取要执行的方法
            func = getattr(self, self.sys_args[1])
            func()  # 调用方法
        else:
            # 没有该方法，打印帮助信息
            self.help_msg("没有方法：%s" % self.sys_args[1])

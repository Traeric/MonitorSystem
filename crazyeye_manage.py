import sys
import os
import django


if __name__ == "__main__":
    # 设置系统的环境变量
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CrazyEye.settings")
    # 让脚本可以操作Django数据库
    django.setup()
    # 生成ArgvHandler对象
    from backend import main
    interactive_obj = main.ArgvHandler(sys.argv)
    # 根据用户参数调用相应的方法
    interactive_obj.call()







from django import template

register = template.Library()


@register.filter
def remainder(arg1, arg2):
    """
    计算两个数的余数
    :param arg1:
    :param arg2:
    :return:
    """
    return arg1 % arg2


@register.simple_tag
def count_host_num(task_obj):
    """
    获取主机成功失败等的个数
    :param task_obj:
    :return:
    """
    # 获取该条记录下所有的主机
    task_detail_objs = task_obj.tasklogdetail_set.all()
    init_num = 0
    success_num = 0
    failed_num = 0
    for task_detail_obj in task_detail_objs:
        if task_detail_obj.status == 0:
            init_num += 1
        elif task_detail_obj.status == 1:
            success_num += 1
        else:
            failed_num += 1
    return [init_num, success_num, failed_num]




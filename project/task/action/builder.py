"""
@Author:叶枫
@Time:2026/9/15
@Desc:自定义action构建器
"""
from project.task.action.custom.lookup_logistics import ActionLookupLogistics
from project.task.action.custom.lookup_order_status import ActionLookupOrderStatus
from project.task.action.register import ActionRegister

# 下面这个方法再depends模块完成注入关系
# 调用ActionRegister方法完成action注册

def register_action(register:ActionRegister):
    register.register_action(ActionLookupLogistics())
    register.register_action(ActionLookupOrderStatus())

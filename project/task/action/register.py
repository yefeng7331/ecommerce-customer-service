"""
@Author:叶枫
@Time:2026/9/15
@Desc:注册操作类
"""
from typing import Any

from task.action.base import ActionResult, Action


class ActionRegister:
    # 初始化字典
    def __init__(self):
        self._actions:dict[str,Any] = {}

    # 注册操作,向字典放action对象
    def register_action(self, action:Action):
        self._actions[action.name] = action


    # 从字典获取action对象的方法
    # 传递yaml中的action名称，返回action对象
    def get_action(self, name:str) ->Any:
        return self._actions.get(name)



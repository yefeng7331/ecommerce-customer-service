"""
@Author:叶枫
@Time:2026/9/15
@Desc:基础操作类
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from domain.state import DialogueState


# 封装yaml的action属性值
@dataclass
class ActionCall:
    # 必须
    action_name: str


# 封装中台接口返回数据
@dataclass
class ActionResult:
    slot_updates: dict[str, Any] = field(default_factory=dict)


# 基础操作类
class Action(ABC):
    # name属性
    name: str = ''

    # 抽象方法,子类要继承action基类，必须实现run方法
    @abstractmethod
    async def run(self, state: DialogueState):
        pass

"""
@Author:叶枫
@Time:2026/9/15
@Desc:查询物流操作类
"""
from config.config import Settings
from domain.state import DialogueState
from task.action.base import Action, ActionResult
from utils.http_client import http_client


class ActionLookupLogistics(Action):
    # name值和yaml中的action_name值保持一致
    name = 'action_lookup_logistics'
    # 实现查询物流操作
    async def run(self, state: DialogueState)->ActionResult:
        order_number = state.tasks.active.slots.get('order_number')

        # 拼接中台查询物流接口地址
        url = f'{Settings.commerce_api_base_url}/orders/{order_number}/logistics'

        # 调用中台查询物流接口,远程调用
        response = await http_client.get(url)
        data = await response.json().get('data','当前订单无数据')
        return ActionResult(slot_updates={
            'logistics_company': data.get('logistics_company','未知公司'),
            'tracking_number': data.get('tracking_number','未知单号'),
            'logistics_status': data.get('status','未知进度'),
        })

"""
加载器模块,用于加载yaml文件，封装到Flow类中
"""
from pathlib import Path

import yaml

from project.task.flow.models import FlowCatalog, Flow, FlowSlot
from project.task.flow.steps import FlowStep


class FlowLoader:
    # 根据yaml文件路径加载yaml文件数据，封装到FlowCatalog对象中
    def load(self, path: Path) -> FlowCatalog:
        # read_text读取文件内容，返回文本
        flow_text = path.read_text(encoding="utf-8")
        # 把读取文本解析成字典格式
        flow_dict = yaml.safe_load(flow_text)
        # 加载槽位(slots)数据
        slots: dict[str, FlowSlot] = self._load_slots(flow_dict["slots"])
        # 加载流程(flows)数据
        flows: dict[str, Flow] = self._load_flows(flow_dict["flows"], slots)

        return FlowCatalog(slots=slots, flows=flows)

    def _load_slots(self, slots_data: dict[str, dict]):
        slots: dict[str, FlowSlot] = {}
        # 遍历slot_data字典，创建FlowSlot对象
        for slot_name, slot_data in slots_data.items():
            # 根据slot_name，把对应slot_data==>FlowSlot对象
            slots[slot_name] = FlowSlot(
                name=slot_name,
                **slot_data
            )
        return slots

    def _load_flows(self, flow_datas: dict[str, dict], slots: dict[str, FlowSlot]) -> dict[str, Flow]:
        flows: dict[str, Flow] = {}
        # 遍历flow_data字典
        for flow_id, flow_data in flow_datas.items():
            # 根据flow_id，把对应flow_data==>Flow对象

            # 槽位数据
            # 封装
            flow_slots:dict[str,FlowSlot] = [
            slots[collect_step['slot_name']]
            for collect_step in flow_data['steps']
                if collect_step['type'] == 'collect']

            # 步骤数据
            steps:list[FlowStep] = [
                FlowStep.from_dict(flow_step)
                for flow_step in flow_data['steps']
            ]

            flow: Flow = Flow(
                id=flow_id,
                description=flow_data['description'],
                steps=steps,
                slots=flow_slots,
                name=flow_data['name']
            )
            flows[flow_id] = flow
        return flows


if __name__ == "__main__":
    loader = FlowLoader()
    path = Path(__file__).parents[3] / "flow_config" / "user_flows.yml"
    flow_catalog = loader.load(path)
    print(flow_catalog)

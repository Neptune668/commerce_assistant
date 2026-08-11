from pathlib import Path
from typing import List, Dict, Any

import yaml

from atguigu.task.flow.flows import FlowsList, Flow, FlowSlot
from atguigu.task.flow.steps import FlowStep, CollectFlowStep


class FlowLoader:
    """
    yml文件加载器：将yml加载成对象
    """

    def load_many(self, paths: List[Path])-> FlowsList:
        """
        加载多个文件
        :param paths:
        :return:
        """

        flows: List[Flow] = []
        slots: Dict[str, FlowSlot] = {}
        for path in paths:
            # 1. 加载单个文件
            single_flows_list = self.load(path)
            # 2. 合并flows
            flows.extend(single_flows_list.flows)
            # 3.slots重名提示
            duplicate_slot_name = set(slots).intersection(single_flows_list.slots)
            if duplicate_slot_name:
                raise ValueError(f"槽位名称 {duplicate_slot_name} 重复")
            # 4. 合slots
            slots.update(single_flows_list.slots)

        return FlowsList(flows=flows, slots=slots)


    def load(self, path) -> FlowsList:
        """
        加载单个文件
        :param path:
        :return:
        """

        # 1. 读取yml -> dict
        with open(path, "r", encoding="utf-8") as f:
            data: Dict[str, Any] = yaml.safe_load(f)

        # 2. 加载slots
        slots: Dict[str, FlowSlot] = self._load_slots(data.get("slots", {}))

        # 3. 加载flows
        flows: List[Flow] = self._load_flows(data.get("flows", {}), slots)

        return FlowsList(flows=flows, slots=slots)


    def _load_slots(self, yaml_slots_data: Dict[str, Any]) -> Dict[str, FlowSlot]:

        slots = {}
        for slot_name, slot_dict in yaml_slots_data.items():
            slots[slot_name] = FlowSlot( name=slot_name,**slot_dict)

        return slots

    def _load_flows(self, yaml_flows_data: Dict[str, Any], slots_definition: Dict[str, FlowSlot]) -> List[Flow]:

        flows: List[Flow] = []
        for flow_id, flow_dict in yaml_flows_data.items():

            steps = [FlowStep.from_dict(step) for step in flow_dict.get("steps", [])]
            flows.append(Flow(
                id=flow_id,
                description=flow_dict.get("description", ""),
                name=flow_dict.get("name", ""),
                steps = steps,
                slots=self._collect_flow_slots(slots_definition, steps)
            ))

        return flows

    def _collect_flow_slots(self, slots_definition: Dict[str, FlowSlot], steps: List[FlowStep]) -> List[FlowSlot]:
        """
        从所有已定义的槽位列表中获取当前流程的所有步骤需要的槽位
        :param slots_definition:
        :param steps:
        :return:
        """
        slot_names = {step.slot_name for step in steps if isinstance(step, CollectFlowStep)}
        return [slots_definition[name] for name in slot_names if name in slots_definition]


if __name__ == '__main__':

    base_path = Path(__file__).parents[3]
    user_flow_path = base_path / "flow_config" / "user_flows.yml"
    system_flow_path = base_path / "flow_config" / "system_flows.yml"
    loader = FlowLoader()
    flows_list = loader.load_many([user_flow_path, system_flow_path])
    print(flows_list)
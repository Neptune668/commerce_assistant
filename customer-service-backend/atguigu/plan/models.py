from enum import Enum
from typing import Any

from pydantic import BaseModel

from atguigu.task.command.models import Command


class TaskTurnPlan(BaseModel):
    commands: list[Command] = []

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TaskTurnPlan":
        return cls(commands=[Command.from_dict(command) for command in data["commands"]])


class KnowledgeTurnPlan(BaseModel):
    intents: list[str] = []  # 意图

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "KnowledgeTurnPlan":
        return cls(intents=data["intents"])


class ChitchatTurnPlan(BaseModel):
    pass


class TurnPlan(BaseModel):
    """
    本轮对话的规划结果
    """
    task: TaskTurnPlan | None = None  # 业务任务的轨道
    knowledge: KnowledgeTurnPlan | None = None  # 信息咨询业务轨道
    chitchat: ChitchatTurnPlan | None = None  # 闲聊业务轨道

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TurnPlan":
        return cls(
            task=TaskTurnPlan.from_dict(data["task"]) if data.get("task") else None,
            knowledge=KnowledgeTurnPlan.from_dict(data["knowledge"]) if data.get("knowledge") else None,
            chitchat=ChitchatTurnPlan() if data.get("chitchat") is not None else None
        )

class ClarifyReason(str, Enum):
    MISSING_TRACK = "missing_track" # 三条轨道都是null
    MULTIPLE_TRACKS = "multiple_tracks" # 填充了两条或以上数量的轨道
    MISSING_TASK_COMMANDS = "missing_task_commands" # 有Task但是没有Command
    MISSING_KNOWLEDGE_INTENT = "missing_knowledge_intent" # 有Knowledge但是没有Intent
    MISSING_FOCUSED_OBJECT = "missing_focused_object" # 知识意图需要聚焦对象，但当前没有或不匹配
    OBJECT_REQUIRES_INTENT = "object_requires_intent" # 用户只发了对象，没说要干嘛
    INVALID_TASK_COMMANDS = "invalid_task_commands" # 模型编了一个Command
    MULTIPLE_TASK_FLOWS = "multiple_task_flows" # 不能同时开启多个任务
    UNKNOWN_TASK_FLOW = "unknown_task_flow" # 模型编了一个Flow

class TurnPlanValidationResult(BaseModel):
    valid: bool # 是否有效
    reason: ClarifyReason | None = None #无效时的原因


if __name__ == '__main__':
    commands_dict = {
        "commands": [
            {"command": "start_flow", "flow": "refund_request"}
        ]
    }
    obj_commands = TaskTurnPlan.from_dict(commands_dict)
    print(obj_commands)


    knowledge_dict = {
        "intents": ["refund_policy"]
    }
    obj_knowledge = KnowledgeTurnPlan.from_dict(knowledge_dict)
    print(obj_knowledge)


    # 对TurnPaln进行反序列化
    turn_plan_dict1 = {
      "task": None,
      "knowledge": {
        "intents": ["refund_policy"]
      },
      "chitchat": None
    }

    turn_plan_obj1 = TurnPlan.from_dict(turn_plan_dict1)
    print(turn_plan_obj1)

    turn_plan_dict2 = {
      "task": {
        "commands": [{"command": "start_flow", "flow": "refund_request"}]
      },
      "knowledge": None,
      "chitchat": None
    }

    turn_plan_obj2 = TurnPlan.from_dict(turn_plan_dict2)
    print(turn_plan_obj2)

    turn_plan_dict3 = {
      "task": None,
      "knowledge": None,
      "chitchat": {}
    }

    if turn_plan_dict3.get("chitchat") is not None:
        print("chitchat")

    turn_plan_obj3 = TurnPlan.from_dict(turn_plan_dict3)
    print(turn_plan_obj3)

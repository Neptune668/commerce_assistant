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

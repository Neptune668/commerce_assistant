# atguigu/task/action/base.py

from abc import ABC, abstractmethod
from typing import Any
from atguigu.domain.state import DialogueState
from atguigu.domain.messages import BotMessage
from pydantic import BaseModel


# 动作的产物
class ActionResult(BaseModel):
    messages: list[BotMessage] = []  # 要发给用户的回复
    slot_updates: dict[str, Any] = {}  # 要写回 state 的槽位


# 所有动作的基类
class Action(ABC):
    name: str  # Action的名字

    @abstractmethod
    async def run(
            self,
            state: DialogueState,
            action_kwargs: dict[str, Any],
    ) -> ActionResult:
        pass

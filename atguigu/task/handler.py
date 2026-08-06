from fastapi.openapi.models import Components

from atguigu.domain.messages import BotMessage
from atguigu.domain.state import DialogueState
from atguigu.task.command.models import Command
from atguigu.task.flow.flows import FlowsList


class TaskHandler:

    def __init__(self, flows: FlowsList):
        self.flows = flows

    async def handle(self, commands: list[Command], state: DialogueState) -> list[BotMessage]:

        # TODO 推进流程的执行

        return [BotMessage(text="AI客服的回答：任务执行完成.....")]
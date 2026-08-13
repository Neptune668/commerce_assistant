from atguigu.api.schemas import HistoryMessage
from atguigu.domain.messages import UserMessage, ProcessResult
from atguigu.domain.state import DialogueState
from atguigu.engine.dialogue_engine import DialogueEngine
from atguigu.prompts.history_builder import HistoryBuilder
from atguigu.repository.dialogue_state_repository import DialogueStateRepository


class DialogueService:
    """
    存算分离的思想：
    存储 dialogue_state_repository
    计算 dialogue_engine
    """

    # 未来通过依赖注入的方式调用__init__ 注入dialogue_state_repository和dialogue_engine
    def __init__(
            self,
            dialogue_state_repository: DialogueStateRepository,
            dialogue_engine: DialogueEngine
    ):
        # 存储
        self.dialogue_state_repository  = dialogue_state_repository
        # 计算
        self.dialogue_engine = dialogue_engine

    async def process_message(self, user_message: UserMessage)-> ProcessResult:
        # self.dialogue_state_repository
        # 调用持久层获取数据
        dialogue_state: DialogueState = await self.dialogue_state_repository.load_state(user_message.sender_id)

        # self.dialogue_engine
        # 调用引擎进行计算
        process_result: ProcessResult = await self.dialogue_engine.process_message(dialogue_state, user_message)

        # self.dialogue_state_repository
        # 调用持久层存储数据
        await self.dialogue_state_repository.save_state(dialogue_state)

        return process_result

    async def load_chat_history(self, sender_id: str) -> list[HistoryMessage]:

        # 1. 从数据库中获取返回值
        state = await self.dialogue_state_repository.load_state(sender_id)

        # 2. 定义要返回的列表
        chat_messages: list[HistoryMessage] = []

        # 3. 组装列表
        for session in state.sessions:
            for turn in session.turns:
                # 组装用户消息
                chat_messages.append(HistoryBuilder.get_user_message(session.session_id, turn.user_message))
                # 组装系统消息
                chat_messages.extend([
                    HistoryBuilder.get_bot_message(session.session_id, b_msg) for b_msg in turn.bot_messages
                ])

        # 4. 返回列表
        return chat_messages


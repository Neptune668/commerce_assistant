from atguigu.domain.messages import UserMessage, ProcessResult, BotMessage
from atguigu.domain.state import DialogueState


class DialogueEngine:


    async def process_message(self, dialogue_state: DialogueState, user_message: UserMessage) -> ProcessResult:

        # TODO
        # 根据user_message的内容，调用LLM进行路由，判断需要执行哪条轨道（业务流程、RAG检索、闲聊），然后执行某一条轨道

        return ProcessResult(
            sender_id=dialogue_state.sender_id,
            message_id=user_message.message_id,
            messages=[
                BotMessage(text="欢迎来到ATGUIGU智能助手！"),
                BotMessage(text="请输入您的问题：")
            ]
        )
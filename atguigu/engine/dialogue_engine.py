import time

from atguigu.domain.messages import UserMessage, ProcessResult, MessageType
from atguigu.domain.state import DialogueState
from atguigu.plan.models import TurnPlan
from atguigu.plan.turn_planner import TurnPlanner
from atguigu.task.handler import TaskHandler


class DialogueEngine:

    def __init__(
            self,
            turn_planner: TurnPlanner,
            task_handler: TaskHandler,
            # knowledge_handler: KnowledgeHandler,
            # chitchat_handler: ChitchatHandler,
            # clarify_responder: ClarifyResponder,
            # turn_plan_validator: TurnPlanValidator
    ) -> None:
        self.turn_planner = turn_planner
        self.task_handler = task_handler
        # self.knowledge_handler = knowledge_handler
        # self.chitchat_handler = chitchat_handler
        # self.clarify_responder = clarify_responder
        # self.turn_plan_validator = turn_plan_validator

    async def process_message(self, dialogue_state: DialogueState, user_message: UserMessage) -> ProcessResult:

        # 根据user_message的内容，调用LLM进行路由，判断需要执行哪条轨道（业务流程、RAG检索、闲聊），然后执行某一条轨道
        # 1 准备会话（如果没有则创建、如果有则获取）
        self._prepare_session(dialogue_state)

        # 2 开启本轮会话（创建Turn对象）
        self._begin_turn(dialogue_state, user_message)

        # 3 判断消息的类型
        if user_message.type is MessageType.TEXT:
            # 3.1 if 处理文本消息，获取AI客服的回复
            messages = await self._handle_text_message(dialogue_state)
        else:
            # 3.2 else 处理对象消息 TODO
            # 澄清、补槽和用户业务流程的执行
            pass

        # 4 提交本轮记录
        # 4.1 将AI客服的回复写入到pending_turn
        dialogue_state.pending_turn.bot_messages.extend(messages)
        # 4.2 将本轮的pending_turn提交到session（将Turn存储在Session的Turn列表中）
        dialogue_state.commit_pending_turn()

        # 5 组装结果并返回
        return ProcessResult(
            sender_id=dialogue_state.sender_id,
            message_id=user_message.message_id,
            messages=messages
        )

    def _prepare_session(self, dialogue_state: DialogueState) -> None:
        """
        获取或初始化session会话
        :param dialogue_state:
        :return:
        """
        # 1. 获取当前会话
        current_session = dialogue_state.current_session()

        # 2. 如果没有会话，则创建一个会话
        if current_session is None:
            dialogue_state.start_session()
            return

        # 3. 判断会话是否过期(1小时)
        now = time.time()
        if now - current_session.last_activity_at > 60 * 60 * 1:
            # 关闭会话
            dialogue_state.close_current_session()
            # 重置dialogue_state的运行状态
            dialogue_state.reset_runtime_state_for_new_session()
            # 创建新会话
            dialogue_state.start_session()
        else:
            # 更新会话（会话续期）
            current_session.last_activity_at = now

    def _begin_turn(self, dialogue_state, user_message):
        """
        开始一个Turn
        :param dialogue_state:
        :param user_message:
        :return:
        """
        dialogue_state.begin_turn(user_message)

    async def _handle_text_message(self, dialogue_state: DialogueState):

        # 使用TurnPlanner理解用户意图（LLM）,并生成本轮对话的计划
        turn_plan: TurnPlan = await self.turn_planner.predict(dialogue_state, self.task_handler.flows)

        # 使用TurnPlanValidator处理是否存在模型理解幻觉 TODO

        # 根据意图识别的结果执行对应的业务逻辑或者对无效意图做澄清处理
        if turn_plan.task is not None:
            return await self.task_handler.handle(
                commands = turn_plan.task.commands,
                state = dialogue_state
            )
        elif turn_plan.knowledge is not None:
            # KnowledgeHandler TODO  占位
            pass
        else:
            # ChitchatHandler TODO
            pass

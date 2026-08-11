from typing import Any

from jinja2 import Template
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from atguigu.domain.messages import BotMessage
from atguigu.domain.state import DialogueState
from atguigu.infrastructure.llm import llm
from atguigu.prompts.history_builder import HistoryBuilder
from atguigu.task.action.base import Action, ActionResult


class ActionResponse(Action):

    """生成AI和对用户的返回信息"""

    name = "action_response"

    async def run(self, state: DialogueState, action_kwargs: dict[str, Any]) -> ActionResult:

        # 获取mode：action的返回值的生成方式，默认是static
        mode = action_kwargs.get("mode", "static")
        
        if mode == "static":

            # 渲染回复信息
            text = action_kwargs["text"]
            rendered_text = self._render_text(text, state)

            # 组织结果
            return ActionResult(messages=[BotMessage(text=rendered_text)])

        elif mode == "rephrase":

            # 1. 渲染参考回复
            text = action_kwargs["text"]
            rendered_text = self._render_text(text, state)

            # 2. 用模型将参考回复进行重写
            prompt_text = action_kwargs["prompt"]
            message = await self._call_llm(prompt_text, state, rendered_text)

            # 3. 组织结果
            return ActionResult(messages=[BotMessage(text=message)])

        else: #mode == "generate":

            # 1. 用模型直接生成答案
            prompt_text = action_kwargs["prompt"]
            message = await self._call_llm(prompt_text, state)

            # 2. 组织结果
            return ActionResult(messages=[BotMessage(text=message)])

        # return ActionResult()

    @staticmethod
    def _render_text(text: str, state: DialogueState) -> str:

        tpl = Template(text)
        result = tpl.render(
            slots = state.active_task.slots if state.active_task else {},
            context=state.active_system_task or state.active_task
        )
        return result

    async def _call_llm(self, prompt_text: str, state: DialogueState, rendered_text: str = "") -> str:

        """使用llm对rendered_text进行重写"""

        # 1. 初始化提示词模板
        prompt = PromptTemplate.from_template(prompt_text)
        # 2. 构建执行链
        chain = prompt | llm | StrOutputParser()
        # 3. 获取聊天历史记录
        history = HistoryBuilder.build(state.current_session().turns)
        # 4. 获取user_message
        user_message = HistoryBuilder.render_user_message(state.pending_turn.user_message)
        bot_message = await chain.ainvoke({
            "history": history,
            "user_message": user_message,
            "current_response": rendered_text
        })

        return bot_message





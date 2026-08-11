from atguigu.domain.messages import BotMessage
from atguigu.knowledge.intents import KnowledgeIntent


class KnowledgeHandler:

    def __init__(self, knowledge_intends: dict[str, KnowledgeIntent]):
        self.knowledge_intends = knowledge_intends

    def handle(self) -> list[BotMessage]:
        """
        处理用户意图
        :return:
        """

        # TODO 进行知识库的查找

        return [BotMessage(text="暂时无法查找.....TODO")]
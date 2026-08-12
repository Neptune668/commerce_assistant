import asyncio
import json
from abc import abstractmethod, ABC
from typing import Any

from pydantic import BaseModel

from atguigu.domain.state import DialogueState
from atguigu.infrastructure.shared import fetch_product, fetch_order, fetch_logistics


class KnowledgeChunk(BaseModel):
    content: str

class KnowledgeProvider(ABC):

    provider_id = ""

    @abstractmethod
    async def retrieve(self, state: DialogueState) -> list[KnowledgeChunk]:
        """
        提供检索方法
        :param state:
        :return:
        """
        pass

class ProductAPIProvider(KnowledgeProvider):

    provider_id = "api.product"

    async def retrieve(self, state: DialogueState) -> list[KnowledgeChunk]:
        product_id = state.focused_object.id
        data: dict[str, Any] = await fetch_product(product_id)
        text = json.dumps(data, ensure_ascii=False, indent=4)
        return [KnowledgeChunk(content=f"商品信息: \n {text}")]

class OrderAPIProvider(KnowledgeProvider):
    provider_id = "api.order"

    async def retrieve(self, state: DialogueState) -> list[KnowledgeChunk]:

        order_number = state.focused_object.id
        order_data, logistics_data = await asyncio.gather(
            fetch_order(order_number),
            fetch_logistics(order_number)
        )

        text = json.dumps({
            "order_number": order_number,
            "order": order_data,
            "logistics": logistics_data
        }, ensure_ascii=False, indent=4)

        return [
            KnowledgeChunk(content=f"订单与物流信息: \n {text}")
        ]

class FAQProvider(KnowledgeProvider):
    provider_id = "faq.default"

    async def retrieve(self, state: DialogueState) -> list[KnowledgeChunk]:

        # TODO 集成 MySQL\Mongo\Elasticsearch
        return [KnowledgeChunk(content="FAQ：未检索到相关问题")]

class RAGProvider(KnowledgeProvider):
    provider_id = "rag.default"

    async def retrieve(self, state: DialogueState) -> list[KnowledgeChunk]:

        # TODO 集成milvus
        return [KnowledgeChunk(content="RAG：未检索到相关信息")]






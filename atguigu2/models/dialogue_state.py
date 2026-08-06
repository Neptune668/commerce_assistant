from sqlalchemy import TEXT
from sqlalchemy.orm import MappedColumn, Mapped

from atguigu2.models.base import Base


class DialogueState(Base):
    __tablename__ = "dialogue_states"
    sender_id: Mapped[str] = MappedColumn(primary_key=True)
    state_json: Mapped[str] = MappedColumn(TEXT, nullable=False, default={})  # 数据库长文本类型
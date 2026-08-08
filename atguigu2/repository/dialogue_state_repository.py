import json

from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert

from sqlalchemy.ext.asyncio import AsyncSession

from atguigu2.domain.state import DialogueState
from atguigu2.models.dialogue_state import DialogueStateRecord


class DialogueStateRepository:
    # session：会话的session对象，依赖注入进来
    # session：会话的session对象，依赖注入进来
    def __init__(self, session: AsyncSession):
        self.session = session

    async def load_state(self, sender_id: str) -> DialogueState:
        # 1. 定义sql
        sql = select(DialogueStateRecord).where(DialogueStateRecord.sender_id == sender_id)
        # 2. 执行sql
        result = await self.session.execute(sql)
        # 3. 获取结果
        state = result.scalar_one_or_none()

        # 4. 数据库中如果有记录则获取
        if state:
            # json str 转换成dict对象
            state_dict = json.loads(state.state_json)
            # dict对象转成python类的对象
            return DialogueState.model_validate(state_dict)

        # 5. 数据库中如果没有记录则创建一个新的状态记录
        return DialogueState(sender_id=sender_id)

    async def save_state(self, dialogue_state: DialogueState):
        # mode="json"???
        # 1. 将对象转成字典
        dict = dialogue_state.model_dump(mode="json")
        # 2. 将字典转成字符串
        state_json = json.dumps(dict)

        # 方案一：使用if判断
        # 基于sender_id查询数据，如果有就是update，如果没有就是insert

        # 方案二：使用on_duplicate_key_update将insert升级为update
        # 3. 向 dialogue_states 数据库表中插入一条记录
        insert_sql = insert(DialogueStateRecord).values(
            sender_id=dialogue_state.sender_id,
            state_json=state_json
        )
        # 4. 前面的insert如果插入失败，则sql自动升级为update语句
        update_sql = insert_sql.on_duplicate_key_update(
            state_json=insert_sql.inserted.state_json
        )
        # 5. 重新执行sql
        await self.session.execute(update_sql)
        # 6. 提交事务
        await self.session.commit()
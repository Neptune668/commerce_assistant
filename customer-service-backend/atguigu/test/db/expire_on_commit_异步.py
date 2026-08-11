import asyncio
from typing import Optional
from sqlalchemy import String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from atguigu.conf.config import settings

# 声明ORM模型的基类，所有数据表实体类继承此类
class Base(DeclarativeBase):
    pass

# 用户实体模型，映射数据库user_account表
class User(Base):
    # 指定映射的数据表名称
    __tablename__ = "user_account"
    # 主键id
    id: Mapped[int] = mapped_column(primary_key=True)
    # 用户昵称，最长30字符，非空
    name: Mapped[str] = mapped_column(String(30))
    # 用户全名，可选字段，允许为空
    fullname: Mapped[Optional[str]]

# 创建异步数据库引擎，加载配置内异步连接地址，echo开启SQL日志输出
engine = create_async_engine(settings.database_url, echo=True)
# 创建异步会话工厂，提交后内存对象不过期 False；（设置为True会报错）
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

async def test():
    # 创建数据库异步会话，with 自动释放连接资源
    async with async_session_factory() as session:
        # 实例化User对象，构造一条用户数据
        sandy = User(
            name="Peter",
            fullname="Peter Cheeks"
        )

        # 将对象加入会话，标记待新增
        session.add(sandy)

        # 异步提交事务，执行INSERT写入数据库
        await session.commit()

        # 打印新增数据的name字段
        print(sandy.name)

# 启动异步事件循环，执行异步函数
asyncio.run(test())

"""
CREATE TABLE user_account (
    id INTEGER NOT NULL AUTO_INCREMENT,
    NAME VARCHAR(30) NOT NULL,
    fullname VARCHAR(30),
    PRIMARY KEY (id)
)
"""
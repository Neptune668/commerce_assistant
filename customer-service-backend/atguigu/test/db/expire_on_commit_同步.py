
from typing import Optional
from sqlalchemy import create_engine, Integer
from sqlalchemy import String
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

# 创建同步数据库引擎，加载配置中的数据库连接地址，echo=True打印原生SQL日志
engine = create_engine(settings.database_url_sync, echo=True)

# 构建会话工厂，提交后内存对象不过期 False； 过期 True
session_factory = sessionmaker(engine, expire_on_commit=False)

# 创建数据库会话，with 自动关闭会话资源
with session_factory() as session:
    # 实例化User对象，构造一条用户数据
    sandy = User(
        name="sandy",
        fullname="Sandy Cheeks"
    )
    # 将对象加入会话，标记待新增
    session.add(sandy)
    # 提交事务，执行insert写入数据库
    session.commit()


    # 打印新增数据的name字段
    print(sandy.name)

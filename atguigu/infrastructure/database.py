import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession

from atguigu.conf.config import settings

# 定义全局的引擎engine
# 定义全局的session工厂
engine: AsyncEngine | None = None
async_session: async_sessionmaker[AsyncSession] | None = None


# 初始化数据库连接资源
def init_db_engine():

    global  engine, async_session

    # 先创建引擎
    engine = create_async_engine(
        settings.database_url,
        echo= True,  # 打印SQL
        # 每次从数据库链接池取出连接之前，先向数据库发送心跳查询（SELECT 1）检查连接是否可用
        # 若连接已断开则自动丢弃当前连接并创建新连接，避免发生连接失效的错误
        pool_pre_ping=True,
    )

    # 再由引擎创建session
    # expire_on_commit=False 默认值是True, 异步场景不起作用会报错,因此需要设置成False
    async_session = async_sessionmaker(engine, expire_on_commit=False)

# 关闭资源
async def close_db_engine():
    if engine is not None:
        await engine.dispose()


if __name__ == '__main__':

    async def test():

        # 初始化引擎
        init_db_engine()

        # 获取session对象
        async with async_session() as session:

            # 使用session访问远程数据库
            result = await session.execute(text("SELECT 1"))

            # data_all = result.fetchall()
            # print(data_all)
            data_one = result.fetchone()
            print(data_one)

        # 关闭引擎
        await close_db_engine()

    asyncio.run(test())
from contextlib import asynccontextmanager

from fastapi import FastAPI

from atguigu.api.routers.chat_router import router
from atguigu.infrastructure.database import init_db_engine, close_db_engine

"""
1. 启动服务： uvicorn启动
2. 执行数据库资源的初始化（引擎，数据库连接池，session工厂对象）
3. 遇到 yield: 暂停当前的 lifespan 函数的执行，交出执行权给 FastAPI框架，原地等待，不会继续执行
4. 此时FastAPI正式启动，开始监听18082端口，接收客户端发送的API请求
5. 当关闭服务器的时候，FastAPI收到服务的关闭信号，通知lifespan继续往下执行
6. 程序从暂停的yield恢复
7. 执行 close_db_engine() 清理数据库资源，服务停止
"""

# FastAPI应用的生命周期管理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    # app：可以挂载一些信息

    print("服务启动....")
    # 初始化数据库连接资源
    init_db_engine() # async_session已经初始化

    yield # 开始接收FastAPI的请求

    await close_db_engine()
    print("服务停止...")


# 挂载生命周期函数
app = FastAPI(description="电商小二", lifespan=lifespan)
app.include_router(router)

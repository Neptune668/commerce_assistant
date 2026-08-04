import uvicorn

from atguigu.conf.config import settings

if __name__ == '__main__':

    # 启动服务
    uvicorn.run(
        app="api.app:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True
    )
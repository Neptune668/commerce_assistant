from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

#配置.env文件的实际路径
ENV_FILE = Path(__file__).parents[2] / ".env"

# 默认情况下pydantic_settings会从系统环境变量中读取配置
class Settings(BaseSettings):
    # LLM
    llm_model: str
    llm_base_url: str
    llm_api_key: str

    # 商城 API
    commerce_api_base_url: str

    # 数据库
    database_url: str
    database_url_sync: str

    # 服务器
    app_host: str
    app_port: int

    # extra = "ignore"：表示.env中配置了，但是当前文件中没有配置，不会报错
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore", env_file_encoding="utf-8")

# 延迟加载
@lru_cache
def get_settings():
    print("初始化Settings")
    return Settings()
settings = get_settings()

# 预加载
# settings = Settings()

if __name__ == '__main__':

    # 读取预加载的配置
    # print(settings.app_port)
    # print(settings.app_port)
    # print(Path(__file__).parents[2] / ".env")

    # 读取延迟加载的配置
    settings = get_settings()
    print(settings.llm_base_url)

    settings = get_settings()
    print(settings.llm_base_url)
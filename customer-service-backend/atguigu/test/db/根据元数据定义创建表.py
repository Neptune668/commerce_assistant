from sqlalchemy import create_engine, Integer
from sqlalchemy import String
from sqlalchemy.sql.schema import MetaData, Table, Column

from atguigu.conf.config import settings


# 创建同步数据库引擎，加载配置中的数据库连接地址，echo=True打印原生SQL日志
engine = create_engine(settings.database_url_sync, echo=True)
# 创建元数据对象
metadata_obj = MetaData()

# 定义表
employees = Table(
    "employees",
    metadata_obj,
    Column("employee_id", Integer, primary_key=True),
    Column("employee_name", String(60), nullable=False, key="name")
)
# 创建表
employees.create(engine)

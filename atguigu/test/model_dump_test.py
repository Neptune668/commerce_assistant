from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str
    age: int
    birthday: datetime
    height: Decimal
    remark: bytes

u1 = User(
    id="1",
    name="张三",
    age=18,
    birthday=datetime(2008, 8, 8, 8, 8, 8),
    height=Decimal("1.75"),
    remark=b"hello",
)
# 序列化后是JSON标准类型，所有类型都会被统一成字符串、数字这些标准类型，方便存数据库、写文件日志或传给 Java、JS 等其他语言、通过http传输。
print(u1.model_dump(mode="json"))

# 默认值：序列化后还是 Python 自己的对象。比如日期还是 datetime 对象、小数还是 Decimal 对象
print(u1.model_dump(mode="python"))

# 什么时候用哪个
# 要 json.dumps()、存数据库、返回给前端 → 用 mode="json"，保证序列化不会报错。
# 还在 Python 内部继续处理用 mode="python"。

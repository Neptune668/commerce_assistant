# atguigu/infrastructure/shared.py

from urllib.parse import quote

from atguigu.conf.config import settings
from atguigu.infrastructure import http_client


def _base_url() -> str:
    """处理url最后的多余的反斜杠"""
    return settings.commerce_api_base_url.rstrip("/")

def _extract_data(result: dict | None) -> dict | None:
    """从API调用的结果中获取出data字段"""
    data = result.get("data") if isinstance(result, dict) else None
    return data if isinstance(data, dict) else None

async def fetch_order(order_id: str) -> dict | None:
    """获取订单信息"""

    try:
        # 1. 调用API
        result = await http_client.http_client.get(f'{_base_url()}/orders/{quote(order_id, safe="")}')

        # 2. 解析data
        return _extract_data(result.json())

    except Exception:
        return None


async def fetch_logistics(order_id: str) -> dict | None:
    """获取物流信息"""

    try:
        # 1. 调用API
        result = await http_client.http_client.get(f'{_base_url()}/orders/{quote(order_id, safe="")}/logistics')

        # 2. 解析data
        return _extract_data(result.json())

    except Exception:
        return None

async def submit_refund_request(order_id: str, reason: str) -> dict | None:
    """提交退款请求"""

    try:
        # 1. 调用API
        result = await http_client.http_client.post(
            f'{_base_url()}/orders/{quote(order_id, safe="")}/refund-applications', json={"reason": reason})

        # 2. 解析data
        return _extract_data(result.json())

    except Exception:
        return None

async def fetch_product(product_id: str) -> dict | None:

    """获取商品信息"""

    try:
        # 1. 调用API
        result = await http_client.http_client.get(f'{_base_url()}/products/{quote(product_id, safe="")}')

        # 2. 解析data
        return _extract_data(result.json())

    except Exception:
        return None


if __name__ == '__main__':
    # order_id = "A-2026/04/08-001"
    # print(f'{_base_url()}/orders/{quote(order_id, safe="")}')


    dict_data = { "detail": "订单 A202604081000 不存在。"}
    print(dict_data.get("data"))



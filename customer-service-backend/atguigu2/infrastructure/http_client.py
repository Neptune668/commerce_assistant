import asyncio
from urllib.parse import quote

import httpx

# 同步方式
# r = httpx.get('http://localhost:18081/users/u1001/orders')
# print(r.json())

# 异步方式
# async def main():
#
#     # with 表示with代码块结束后自动调用close方法，关闭远程请求
#     async with httpx.AsyncClient() as client:
#         response = await client.get('http://localhost:18081/users/u1001/orders')
#         print(response.json())
#
# asyncio.run(main())


# 优化
# 定义全局变量
http_client: httpx.AsyncClient | None = None


# 初始化http客户端
def init_http_client():
    global http_client
    http_client = httpx.AsyncClient()

# 关闭资源
async def close_http_client():
    if http_client is not None:
        await http_client.aclose()


if __name__ == '__main__':

    async def test():
        init_http_client()
        result = await http_client.get('http://localhost:18081/users/u1001/orders')
        print(result.json())
        await  close_http_client()

    async def test_get_order():
        init_http_client()
        order_id = "A20260410001"
        result = await http_client.get(f'http://localhost:18081/orders/{quote(order_id, safe="")}')

        data = result.json()
        print(data)
        await  close_http_client()

    asyncio.run(test_get_order())
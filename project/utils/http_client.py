"""
@Author:叶枫
@Time:2026/9/8
@Desc: HTTP服务器
        模块作用：启动HTTP服务器，提供HTTP接口,创建远程调用httpx工具类
"""
import asyncio

from httpx import AsyncClient

# 定义变量
http_client:AsyncClient | None = None

# 创建两个方法
# 初始化方法
def init_http_client():
    global http_client
    http_client = AsyncClient(timeout=10.0)

# 关闭方法
async def close_http_client():
    await http_client.aclose()

# 测试方法
async def test():
    init_http_client()
    # restful风格： 查询get 添加post 修改put 删除delete
    response = await http_client.get("http://127.0.0.1:18081/users/u1001/orders")
    print(response.json())
    

if __name__ == "__main__":
    asyncio.run(test())
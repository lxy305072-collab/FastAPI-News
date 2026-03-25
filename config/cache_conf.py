import json
from typing import Any

import redis.asyncio as redis


# 定义全局变量，方便修改
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0

#创建redis的连接对象
redis_client = redis.Redis(
    host=REDIS_HOST, # redis服务地址
    port=REDIS_PORT, # redis端口
    db=REDIS_DB,     # redis数据库编号(默认为0)，0~15
    decode_responses=True  # 将数据解码为字符串
)

#缓存操作就是围绕Redis 做“存、取、删、判断、过期”等操作,让数据访问更快、数据库压力更小。
# Redis 存储数据:key-value
#
# 方法                      参数                            描述
#                         key: str,
# setex                   expire: int(秒),           设置缓存并指定过期时间(秒)
#                         value: str
#
# get                    key: str                   获取缓存值。若缓存不存在,返回 None
#
# delete                 key: str                    删除指定的缓存键
#
# exists                  key: str                   检查缓存键是否存在,返回布尔值




# 设置 和 读取（字符串 和 列表或字典）"[{}]"
# 读取：字符串
async def get_cache(key: str):
    """
    获取缓存值
    :param key:
    :return:
    """
    try:
        return await redis_client.get(key)  #根据你传入的 key（字符串），从 Redis 中获取这个 key 对应的 value 值
    except Exception as e:
        print(f"获取缓存值失败：{e}")
        return None


# 读取：列表或字典
async def get_json_cache(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data) # 提取列表或字典格式数据，去除括号
        return None
    except Exception as e:
        print(f"获取json缓存值失败：{e}")
        return None


# 设置缓存 setex(key, expire过期时间这里设为3600秒, value)
async def set_cache(key: str, value: Any,expire: int = 3600):  #默认形参放非默认后，否则报错
    """
    设置缓存
    :param key:
    :param expire:
    :param value:
    :return:
    """
    try:
        if isinstance(value, (list, dict)):
            # 将列表或字典转换为 JSON 字符串
            value = json.dumps(value, ensure_ascii=False) # ensure_ascii=False 保留中文
        await redis_client.setex(name=key, time=expire, value=value)
    except Exception as e:
        print(f"设置缓存失败：{e}")
        return None








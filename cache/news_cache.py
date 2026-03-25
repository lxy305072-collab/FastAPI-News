# 新闻相关的缓存方法：新闻分类的读取和写入
# key - value
from typing import List, Dict, Any, Optional

from config.cache_conf import get_json_cache, set_cache

CATEGORIES_KEY = "news:categories"
NEWS_LIST_PREFIX = "news_list:"
NEWS_DETAIL_PREFIX = "news:detail:"
RELATED_NEWS_PREFIX = "news:related:"



# 获取新闻分类缓存
async def get_cached_categories():

    return await get_json_cache(CATEGORIES_KEY)

# 写入新闻分类缓存:缓存的数据，过期时间
# 分类、配置 7200；列表： 600； 详情： 1800；验证码：120 -- 数据越稳定，缓存越持久
# 避免所有key同时过期 引起缓存雪崩
async def set_cached_categories(data: List[Dict[str, Any]], expire: int = 7200):
    return await set_cache(CATEGORIES_KEY, data, expire)





# 确保唯一性，key设计为 前缀 + 分类id:页码:每页数量
# 写入新闻列表缓存 key = news_list:分类id:页码:每页数量  + 列表数据 + 过期时间
async def set_cache_news_list(category_id: Optional[int], page: int, size:int, new_list: List[Dict[str, Any]], expire: int = 1800):
    # 调用 封装的 Redis 的设置方法，存新闻列表到缓存
    category_part = category_id if category_id is not None else "all"  #如果没有id视为全部分类
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"
    return await set_cache(key, new_list, expire)

# 读取缓存——新闻列表
async def get_cache_news_list(category_id: Optional[int], page: int, size:int):
    category_part = category_id if category_id is not None else "all"  # 如果没有id视为全部分类
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"
    return await get_json_cache(key)






# 写入新闻详情缓存
async def set_cache_news_detail(news_id: int, news_detail: Dict[str, Any], expire: int = 1800)-> bool:
    key = f"{NEWS_DETAIL_PREFIX}{news_id}"
    return await set_cache(key, news_detail, expire)

# 读取新闻详情缓存
async def get_cache_news_detail(news_id: int):
    key = f"{NEWS_DETAIL_PREFIX}{news_id}"
    return await get_json_cache(key)





#缓存相关新闻列表
async def set_cache_related_news(news_id: int, category_id: int, related_list: List[Dict[str, Any]], expire: int = 1800):

    key = f"{RELATED_NEWS_PREFIX}{news_id}:{category_id}"
    return await set_cache(key, related_list, expire)


#获取缓存的相关新闻列表
async def get_cached_related_news(news_id: int, category_id: int):

    key = f"{RELATED_NEWS_PREFIX}{news_id}:{category_id}"
    return await get_json_cache(key)













# todo：数据库增删改查
# todo：把数据库操作逻辑抽离出来，让路由层只负责接口逻辑，不直接写 SQL
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from cache.news_cache import get_cached_categories, set_cached_categories, get_cache_news_list, set_cache_news_list, \
    get_cache_news_detail, set_cache_news_detail, get_cached_related_news, set_cache_related_news
from models.news import Category,News
from schemas.base import NewsItemBase
from schemas.news import NewsDetailResponse, RelatedNewsResponse


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    """获取新闻分类"""
    #先从缓存中获取数据
    cache_categories = await get_cached_categories()
    if cache_categories:
        return cache_categories

    #没有则查库寻找
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt) #execute方法把 SQL 语句 / 查询对象（比如这里的stmt）发送给数据库执行，并返回结果
    categories = result.scalars().all() #ORM结果

    #写入缓存
    if categories:
        categories = jsonable_encoder(categories) #把ORM结果转为JSON
        await set_cached_categories(categories)





async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    """获取新闻列表"""

    #先从缓存中获取数据
    # 跳过的数量skip = (页码 -1) * 每页数量 → 页码 = 跳过的数量 // 每页数量 + 1
    # await get_cache_news_list(分类id, 页码, 每页数量)
    page = skip // limit + 1
    cache_list =await get_cache_news_list(category_id, page, limit) #缓存中获取数据
    if cache_list:
        # return cache_list #要返回orm格式 方便参与 ORM 相关操作
        return [News(**item) for item in cache_list]

    # 查询指定分类下的所有新闻
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit) #skip 跳过前skip个,limit 限制每页的数量
    result = await db.execute(stmt)
    news_list =  result.scalars().all()

    #写入缓存
    if news_list:
        # 先把orm数据转为JSON才能写入缓存
        # 先把 ORM 数据 转换 字典才能写入缓存
        # ORM 转成 Pydantic，再转为 字典
        # by_alias=False 不适用别名，保存 Python 风格，因为 Redis 数据是给后端用的
        news_data = [NewsItemBase.model_validate(item).model_dump(mode="json", by_alias=False) for item in news_list]
        await set_cache_news_list(category_id, page, limit, news_data)

    return news_list






async def get_news_count(db: AsyncSession, category_id: int):
    """查询指定分类下的新闻总数量"""
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()  #scalar_one() 只能有一个结果,否则报错，方便排查数据库是否有多个结果







async def get_news_detail(db: AsyncSession, news_id: int):
    """获取指定新闻细节内容"""
    # 先尝试从缓存获取
    cached_news = await get_cache_news_detail(news_id)
    if cached_news:

        return News(**cached_news)  #把缓存的字典数据转成 News ORM 模型对象

    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    news = result.scalar_one_or_none()

    # 存入缓存（不使用别名，保持数据库字段名）
    if news:
        # 先把orm数据转为JSON才能写入缓存
        # 先把 ORM 数据 转换 字典才能写入缓存
        # ORM 转成 Pydantic，再转为 字典
        # by_alias=False 不适用别名，保存 Python 风格，因为 Redis 数据是给后端用的
        news_dict = NewsDetailResponse.model_validate(news).model_dump(
            by_alias=False, mode="json", exclude={'related_news'}
        )
        await set_cache_news_detail(news_id, news_dict)

    return news




async def increase_news_views(db: AsyncSession, news_id: int):
    """新闻浏览量+1"""
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    # 返回更新数量--》检查数据库是否真的命中了数据 --》命中了返回True
    return result.rowcount > 0 #rowcount表示 “这次数据库操作影响的行数”






async def get_related_news(db: AsyncSession, news_id: int , category_id: int ,limit: int = 5):
    """获取相关新闻"""
    cached_related = await get_cached_related_news(news_id, category_id)
    if cached_related:
        # 缓存数据是字典列表，直接返回
        return cached_related

    stmt = select(News).where(
        News.category_id == category_id,
        News.id != news_id      #排除当前新闻
    ).order_by(
        News.views.desc(),               #按浏览量排序  desc()降序，大的排前面
        News.publish_time.desc() #按发布时间排序
    ).limit(limit)
    result = await db.execute(stmt)
    related_news = result.scalars().all()

    # 转换为字典格式用于缓存和返回（不使用别名，保持数据库字段名）
    if related_news:
        related_data = [
            RelatedNewsResponse.model_validate(news).model_dump(by_alias=False, mode="json")
            for news in related_news
        ]
        await set_cache_related_news(news_id, category_id, related_data)
        return related_data
    # 没有相关新闻，返回空列表
    return []

    # return [
    #     {
    #         "id": news_detail.id,
    #         "title": news_detail.title,
    #         "content": news_detail.content,
    #         "image": news_detail.image,
    #         "author": news_detail.author,
    #         "publishTime": news_detail.publish_time,
    #         "categoryId": news_detail.category_id,
    #         "views": news_detail.views
    #     }  for news_detail in related_news]  #列表推导式 基于全量数据推导出新闻的核心数据




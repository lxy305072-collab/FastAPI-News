#CRUD 操作封装
# todo：数据库增删改查
# todo：把数据库操作逻辑抽离出来，让路由层只负责接口逻辑，不直接写 SQL
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category,News



async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    """获取新闻分类"""
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt) #execute方法把 SQL 语句 / 查询对象（比如这里的stmt）发送给数据库执行，并返回结果
    return result.scalars().all()


async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    """获取新闻列表"""
    stmt = select(News).offset(skip).limit(limit) #skip 跳过前skip个,limit 限制每页的数量
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_news_count(db: AsyncSession, category_id: int):
    """查询指定分类下的新闻总数量"""
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()  #scalar_one() 只能有一个结果,否则报错，方便排查数据库是否有多个结果


async def get_news_detail(db: AsyncSession, news_id: int):
    """获取指定新闻细节内容"""
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()  #scalar_one_or_none() 允许有一个结果，否则返回None



async def increase_news_views(db: AsyncSession, news_id: int):
    """新闻浏览量+1"""
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    # 返回更新数量--》检查数据库是否真的命中了数据 --》命中了返回True
    return result.rowcount > 0 #rowcount表示 “这次数据库操作影响的行数”


async def get_related_news(db: AsyncSession, news_id: int , category_id: int ,limit: int = 5):
    """获取相关新闻"""
    stmt = select(News).where(
        News.category_id == category_id,
        News.id != news_id      #排除当前新闻
    ).order_by(
        News.views.desc(),               #按浏览量排序  desc()降序，大的排前面
        News.publish_time.desc() #按发布时间排序
    ).limit(limit)
    result = await db.execute(stmt)
    # return result.scalars().all()
    related_news = result.scalars().all()
    return [
        {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time,
            "categoryId": news_detail.category_id,
            "views": news_detail.views
        }  for news_detail in related_news]  #列表推导式 基于全量数据推导出新闻的核心数据




from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class NewsItemBase(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    author: Optional[str] = None
    category_id: int = Field(alias="categoryId")
    views: int
    publish_time: Optional[datetime] = Field(None, alias="publishedTime")

    model_config = ConfigDict(
        from_attributes=True,
        ## 假设 db_news 是 SQLAlchemy 的 ORM 对象（有 id、title、category_id 等属性）
        # db_news = await db.query(News).filter(News.id == 1).first()
        # # 直接转换为 Pydantic 模型（无需手动转字典）
        # news_item = NewsItemBase.model_validate(db_news)
        populate_by_name=True # 支持通过「字段名」或「别名」赋值
)

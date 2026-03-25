
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_db
from crud import favorite
from models.users import User
from schemas.favorite import FavoriteCheckResponse, FavoriteAddResponse, FavoriteListResponse
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/favorite", tags=["favorite"])


@router.get("/check")
async def check_favorite(
        news_id: int=Query(...,alias="newsId"),
        user: User=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    is_favorite = await favorite.is_news_favorite(db, user.id, news_id)
    return success_response(message="检查收藏状态成功",data=FavoriteCheckResponse(isFavorite=is_favorite))



@router.post("/add")
async def add_favorite(
        data: FavoriteAddResponse,
        user: User=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await favorite.add_news_favorite(db, user.id, data.news_id)
    return success_response(message="收藏成功",data=result)



@router.delete("/remove")
async def remove_favorite(
        news_id: int=Query(...,alias="newsId"),
        user: User=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await favorite.remove_news_favorite(db, user.id, news_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="收藏记录不存在")
    return success_response(message="取消收藏成功")



# 获取收藏列表
@router.get("/list")
async def get_favorite_list(
        page: int=Query(1,ge=1),
        page_size: int=Query(10,ge=1,le=100,alias="pageSize"),
        user: User=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    rows, total =await favorite.get_favorite_list(db, user.id, page, page_size)
    #将数据库查询返回的元组数据（news 对象、收藏时间、收藏 ID），转换成前端易于使用的字典格式列表
    favorite_list = [{
         **news.__dict__,  #__dict__ 是 Python 对象的内置属性，会返回对象的属性 - 值字典
         "favorite_time": favorite_time,
         "favorite_id": favorite_id
        }for news,favorite_time,favorite_id in rows]
    has_more = total > page * page_size

    data = FavoriteListResponse(list=favorite_list,total=total,hasMore=has_more)
    return success_response(message="获取收藏列表成功",data=data)



@router.delete("/clear")
async def clear_favorite(
        user: User=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await favorite.remove_all_favorite(db, user.id)
    return success_response(message=f"清空了{result}条记录")






















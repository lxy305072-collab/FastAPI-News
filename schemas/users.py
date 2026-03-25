from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserRequest(BaseModel):
    username: str
    password: str


#user_info对应的类 ：基础类（可选） + Info类（id、用户名）

class UserInfoBase(BaseModel):
    """
    用户信息基础数据模型
    """
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")


#Info类
class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    # 模型类配置
    model_config = ConfigDict(
        # 允许从orm对象中取值
        from_attributes=True
    )

# success_response的 data 数据类型
class UserAuthResponse(BaseModel):
    token: str
    user_info:UserInfoResponse = Field(...,alias="userInfo")

    #模型类配置
    model_config = ConfigDict(
        # 兼容别名和字段名
        populate_by_name=True,
        # 允许model_validate从orm对象中取值
        from_attributes= True
    )


#更新用户信息的模型类
class UserUpdateRequest(BaseModel):
    nickname: str = None
    avatar: str = None
    gender: str = None
    bio: str = None


#修改用户密码
class UserUpdatePasswordRequest(BaseModel):
    old_password: str = Field(..., alias="oldPassword", description="旧密码")
    new_password: str = Field(..., min_length=6, alias="newPassword", description="新密码")






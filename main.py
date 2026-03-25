from fastapi import FastAPI
from routers import news, users, favorite, history
from fastapi.middleware.cors import CORSMiddleware

from utils.exception_handlers import register_exception_handlers

app = FastAPI()

#注册异常处理器
register_exception_handlers(app)

# 同源的三个条件：协议，域名，端口,满足同源条件才能发请求
# 配置CORS，解决跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # 设置允许的源,*表示所有源都可以访问，工作环境需要指定源
    allow_credentials=True, # 允许发送cookie
    allow_methods=["*"],    # 允许的请求方法
    allow_headers=["*"],    # 允许的请求头
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


#挂载路由/注册路由
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)

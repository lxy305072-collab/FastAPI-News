# 头条新闻后端项目

## 项目简介

这是一个基于FastAPI框架开发的新闻应用后端系统，提供新闻浏览、用户管理、收藏和历史记录等功能。

## 技术栈

- **Web框架**：FastAPI
- **ORM**：SQLAlchemy (异步模式)
- **数据验证**：Pydantic
- **缓存**：Redis
- **认证**：JWT
- **数据库**：MySQL

## 项目结构

```
toutiao_project/
├── main.py              # 主应用文件
├── routers/             # 路由模块
│   ├── news.py          # 新闻相关路由
│   ├── users.py         # 用户相关路由
│   ├── favorite.py      # 收藏相关路由
│   └── history.py       # 历史记录相关路由
├── config/              # 配置文件
│   └── db_config.py     # 数据库配置
├── crud/                # 数据库操作
│   ├── news.py          # 新闻相关操作
│   ├── news_cache.py    # 新闻缓存操作
│   ├── users.py         # 用户相关操作
│   ├── favorite.py      # 收藏相关操作
│   └── history.py       # 历史记录相关操作
├── models/              # 数据库模型
│   ├── __init__.py
│   └── users.py         # 用户模型
├── schemas/             # 数据验证模型
│   ├── users.py         # 用户相关模型
│   ├── favorite.py      # 收藏相关模型
│   └── history.py       # 历史记录相关模型
└── utils/               # 工具函数
    ├── auth.py          # 认证相关
    ├── response.py      # 响应处理
    └── exception_handlers.py  # 异常处理
```

## 主要功能

### 1. 新闻管理

- 获取新闻分类列表
- 获取新闻列表（支持分页和分类筛选）
- 获取新闻详情（自动增加浏览量）
- 获取相关新闻推荐

### 2. 用户管理

- 用户注册
- 用户登录
- 获取用户信息
- 更新用户信息
- 修改密码

### 3. 收藏管理

- 检查新闻是否已收藏
- 添加新闻到收藏
- 取消新闻收藏
- 获取收藏列表（支持分页）
- 清空收藏

### 4. 历史记录管理

- 添加浏览历史
- 获取历史记录列表（支持分页）
- 删除历史记录
- 清空历史记录

## API接口

### 新闻相关

- `GET /api/news/categories` - 获取新闻分类
- `GET /api/news/list` - 获取新闻列表
- `GET /api/news/detail` - 获取新闻详情

### 用户相关

- `POST /api/user/register` - 用户注册
- `POST /api/user/login` - 用户登录
- `GET /api/user/info` - 获取用户信息
- `PUT /api/user/update` - 更新用户信息
- `PUT /api/user/password` - 修改密码

### 收藏相关

- `GET /api/favorite/check` - 检查收藏状态
- `POST /api/favorite/add` - 添加收藏
- `DELETE /api/favorite/remove` - 取消收藏
- `GET /api/favorite/list` - 获取收藏列表
- `DELETE /api/favorite/clear` - 清空收藏

### 历史记录相关

- `POST /api/history/add` - 添加历史记录
- `GET /api/history/list` - 获取历史记录列表
- `DELETE /api/history/delete/{history_id}` - 删除历史记录
- `DELETE /api/history/clear` - 清空历史记录

## 项目特点

1. **异步处理**：使用FastAPI的异步特性和SQLAlchemy的异步模式，提高系统性能
2. **缓存机制**：使用Redis缓存热点数据，减少数据库压力
3. **JWT认证**：实现无状态认证，提高系统安全性
4. **模块化设计**：清晰的代码结构，便于维护和扩展
5. **数据验证**：使用Pydantic进行数据验证，确保数据完整性
6. **异常处理**：统一的异常处理机制，提供友好的错误提示

## 快速开始

### 后端项目

1. 安装依赖

```bash
pip install -r requirements.txt
```

1. 配置数据库连接

修改 `config/db_config.py` 中的数据库连接信息

1. 启动应用

```bash
uvicorn main:app --reload
```

1. 访问API文档

浏览器打开 `http://localhost:8000/docs` 查看API文档

### 前端项目

前端项目是一个独立的项目文件，在frontend文件夹中：

1. 进入前端项目目录

```bash
cd /path/to/frontend/project
```

1. 安装依赖

```bash
Node.js
```

1. 配置API地址

修改前端项目中的API配置文件，将API地址指向后端服务地址（默认为 `http://localhost:8000`）

1. 启动前端开发服务器

```bash
# 使用npm
npm run dev
```

1. 访问前端应用

浏览器打开前端开发服务器地址（通常为 `http://localhost:3000` 或 `http://localhost:5173`）

#### 后端部署

1. 安装依赖

```bash
pip install -r requirements.txt
```

1. 启动应用（生产环境）

```bash
# 使用gunicorn（推荐）
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

# 或使用uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 注意事项

- 本项目使用了Redis作为缓存，请确保Redis服务已启动
- 本项目使用了MySQL作为数据库，请确保MySQL服务已启动并创建了相应的数据库
- 本项目在开发环境中使用了CORS中间件允许所有跨域请求，生产环境中应根据实际情况配置

## 许可证

本项目采用MIT许可证

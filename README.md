# ChanSheen API Service

基于 FastAPI 开发的后端 API 服务，提供用户认证和中国节假日查询接口，支持异步数据库访问。

---

## 目录

- [项目简介](#项目简介)
- [技术栈](#技术栈)
- [环境配置](#环境配置)
- [安装运行](#安装运行)
- [接口文档](#接口文档)
- [接口说明](#接口说明)
- [版本更新](#版本更新)
- [后续计划](#后续计划)
- [许可证](#许可证)

---

## 项目简介

ChanSheen API Service 是一个轻量、高性能的后台服务，主要实现了：

- 基于 JWT 的用户认证体系
- 节假日查询接口，支持按日期查询中国法定节假日及调休信息
- 支持从 JSON 文件和数据库两种方式读取节假日数据
- 使用异步 SQLAlchemy 和 asyncmy 连接 MySQL，提高并发性能

---

## 技术栈

- Python 3.11+
- FastAPI
- SQLAlchemy Async ORM
- asyncmy (MySQL 异步驱动)
- passlib (密码加密)
- python-jose (JWT 认证)
- python-dotenv (环境变量管理)
- slowapi（限流）
- Uvicorn 作为 ASGI 服务器

---

## 环境配置

请在项目根目录新建 `.env` 文件，示例如下：

```dotenv
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=chansheen

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120
```

## 安装运行
1. 克隆仓库并进入项目目录
```bash
git clone https://github.com/HSHanChen/chansheen-api-service.git
cd chansheen-api-service
```

2. 创建虚拟环境并激活（可选）

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

4. 启动项目
```bash
python run.py
```
默认监听地址为 http://0.0.0.0:8001

## 接口文档
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## 接口说明
### 认证模块
- POST /api/auth/token
    请求参数：用户名、密码
    返回：JWT 访问令牌

- GET /api/auth/me
    需要认证，获取当前登录用户信息

### 日历模块
- GET /api/calendar?date=YYYY-MM-DD
    查询指定日期的节假日信息，返回字段包括：
    - date：日期 
    - dateType：日期类型（1=工作日，2=调休假，3=法定节假日） 
    - weekName：星期几 
    - note：备注 
    - lunar：农历信息

## 版本更新

版本号	日期	变更内容
1.0.0	2025-06-15	初始版本，节假日数据从 JSON 文件读取
1.0.1	2025-06-17	节假日数据改为从数据库异步读取，支持 SQLAlchemy AsyncSession

## 后续计划

- 增加节假日维护后台管理系统

- 支持多用户角色权限管理

- 添加更多节日及节气查询接口

- 统一日志管理与错误监控

- 提供 Docker 镜像部署方案

- 许可证
  本项目采用 MIT 许可证，详情见 LICENSE 文件。

## 联系方式
作者：Chan Sheen
邮箱：hschenhan@gmail.com
GitHub: https://github.com/HSHanChen/chansheen-api-service
感谢使用 ChanSheen API Service，欢迎反馈与贡献！
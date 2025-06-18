
# ChanSheen API Service / 禅绅 API 服务

## 📌 项目简介 | Project Introduction

本项目是一个基于 **FastAPI** 构建的轻量级 API 服务，支持令牌验证、节假日查询、用户认证等功能。适用于企业内部系统、HR 接口对接、日历服务等应用场景。

This project is a lightweight API service built with **FastAPI**, featuring token-based authentication, holiday queries, and user login functionality. It is suitable for enterprise systems, HR integrations, and calendar services.

---

## 🆚 版本变更 | Version History

| 版本号 | 说明 (中文) | Description (English) |
|--------|-------------|------------------------|
| 1.0.0  | 基于本地 JSON 文件提供节假日接口和用户验证功能。<br>Holiday API and user auth from local JSON file. |
| 1.0.1  | 节假日和用户数据改为从数据库读取，采用 SQLAlchemy Async 实现异步 ORM 操作。<br>Holiday & user data now retrieved from the database using SQLAlchemy Async ORM. |

---

## 🚀 快速开始 | Quick Start

### 🧱 安装依赖 | Install Dependencies

```bash
pip install -r requirements.txt
```

### ▶️ 运行项目 | Run the Project

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

或者使用 systemd 启动服务：

```bash
sudo systemctl start chansheenapi.service
```

---

## 🔐 用户认证 | User Authentication

通过 `/api/auth/token` 获取访问 Token：

### 请求 | Request

`POST /api/auth/token`

请求体 (表单格式)：

```bash
username=admin&password=admin
```

### 响应 | Response

```json
{
  "access_token": "xxx.yyy.zzz",
  "token_type": "bearer"
}
```

---

## 📅 节假日接口 | Holiday API

### 查询节假日 | Query Holiday

接口地址：

```
GET /api/calendar
```

支持查询参数：

- `year=2025`
- `month=2025-06`
- `date=2025-06-18`

请求需附带认证 Token：

```
Authorization: Bearer <your_token>
```

### 示例响应 | Example Response

```json
{
  "data": [
    {
      "date": "2025-06-18",
      "dateType": 1,
      "weekName": "星期三",
      "note": "工作日",
      "lunar": "五月廿三"
    }
  ]
}
```

---

## ⚙️ 配置说明 | Configuration

环境变量保存在 `.env` 文件中：

```env
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=holiday_db

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120
```

---

## 🗃️ 数据库结构 | Database Schema

### 表：holidays

| 字段名    | 类型     | 说明           |
|-----------|----------|----------------|
| date      | DATE     | 日期           |
| dateType  | TINYINT  | 日期类型（1 正常工作日，2 休息日，3 法定节假日） |
| weekName  | VARCHAR  | 星期名称       |
| note      | TEXT     | 备注说明       |
| lunar     | VARCHAR  | 农历日期       |

### 表：users

| 字段名    | 类型     | 说明     |
|-----------|----------|----------|
| username  | VARCHAR  | 用户名   |
| password  | VARCHAR  | 加密密码 |

---

## 📦 接口文档 | API Documentation

FastAPI 自动生成的接口文档地址如下：

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📬 联系方式 | Contact

如需支持或合作，请联系：

- 📧 邮箱：`justin.han@example.com`
- 🌐 GitHub: [https://github.com/HSHanChen/chansheen-api-service](https://github.com/HSHanChen/chansheen-api-service)

---

## 📄 许可证 | License

本项目采用 MIT 开源许可证。  
This project is licensed under the **MIT License**.

详细信息请参见项目根目录下的 `LICENSE` 文件。  
See the `LICENSE` file for details.

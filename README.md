# Halo API Service with Dynamic JWT Token

## 功能说明

- 用户通过用户名密码获取 JWT Token
- 日历接口需在请求头带 Authorization: Bearer <token> 才能访问
- 用户名密码存在本地 JSON 文件，可替换为数据库

## 运行说明

1. 安装依赖
```
pip install -r requirements.txt
```

2. 运行服务
```
python run.py
```

3. 认证接口获取 token（POST）
```
POST /api/auth/token
Content-Type: application/x-www-form-urlencoded

username=admin&password=admin123
```

4. 带 token 调用日历接口（GET）
```
GET /api/calendar?date=2025-10-01
Header: Authorization: Bearer <token>
```

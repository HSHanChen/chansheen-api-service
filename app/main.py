import traceback
import logging
import sys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from app.routes import calendar, auth
from app.core.limiter import limiter

# ✅ 设置全局 logger
logger = logging.getLogger("mylogger")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# ✅ 创建 FastAPI 实例
app = FastAPI(title="ChanSheen's API Service")
app.state.limiter = limiter

# ✅ 注册中间件（放前面，确保能拦截所有请求）
@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    logger.info(f"👉 请求开始: {request.method} {request.url}")
    try:
        response = await call_next(request)
    except Exception as e:
        traceback.print_exc()
        logger.error(f"❌ 请求处理异常: {str(e)}")
        return JSONResponse(status_code=500, content={"detail": str(e)})
    logger.info(f"✅ 请求结束: {request.method} {request.url} - 状态码: {response.status_code}")
    return response

# ✅ 注册限流异常处理器
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "请求过于频繁，请稍后再试"}
    )

# ✅ 注册路由（最后）
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(calendar.router, prefix="/api/calendar", tags=["日历"])

print("🌟 FastAPI 应用启动中……")

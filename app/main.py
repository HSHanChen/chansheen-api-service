import logging
import sys
import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from app.routes import calendar, auth
from app.core.limiter import limiter

# 日志配置
logger = logging.getLogger(__name__)

# 创建 FastAPI 实例
app = FastAPI(
    title="ChanSheen's API Service",
    docs_url="/docs",   # Swagger UI
    redoc_url="/redoc", # ReDoc
    openapi_url="/openapi.json",
    description="ChanSheen's API Service. If you want to use the api service, pls contact hschenhan@gmail.com",
    version="1.0.1"
)

# 中间件
@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    logger.info(f"请求开始: {request.method} {request.url}")
    try:
        response = await call_next(request)
    except Exception as e:
        traceback.print_exc()
        logger.error(f"请求处理异常: {str(e)}")
        return JSONResponse(status_code=500, content={"detail": str(e)})
    logger.info(f"请求结束: {request.method} {request.url} - 状态码: {response.status_code}")
    return response

# 限流器
app.state.limiter = limiter
# 限流异常处理器
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "请求过于频繁，请稍后再试"}
    )

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(calendar.router, prefix="/api/calendar", tags=["日历"])

@app.on_event("startup")
async def startup_event():
    print("ChanSheen's API Service Start Completed！")
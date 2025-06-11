from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from app.routes import calendar, auth
from app.core.limiter import limiter


app = FastAPI(title="ChanSheen's API Service")
app.state.limiter = limiter
# 限流超出时的处理
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "请求过于频繁，请稍后再试"}
    )

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(calendar.router, prefix="/api/calendar", tags=["日历"])

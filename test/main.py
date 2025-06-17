"""
@Author: Chan Sheen
@Date: 2025/6/17 14:39
@File: main.py
@Description: 
"""
from fastapi import FastAPI, Request
import logging
import sys

app = FastAPI()

logger = logging.getLogger("mylogger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    logger.info(f"👉 请求开始: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"✅ 请求结束: {request.method} {request.url} - 状态码: {response.status_code}")
    return response

@app.get("/ping")
async def ping():
    return {"message": "pong"}


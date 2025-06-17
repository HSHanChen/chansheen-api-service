"""
@Author: Chan Sheen
@Date: 2025/6/16 16:55
@File: database.py
@Description: 
"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_database_url() -> str:
    DB_USER = os.getenv("DB_USER")
    raw_password = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    if not all([DB_USER, raw_password, DB_HOST, DB_PORT, DB_NAME]):
        raise ValueError("Database environment variables are not set")

    DB_PASSWORD = quote_plus(raw_password)
    return f"mysql+asyncmy://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

DATABASE_URL = get_database_url()
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

# ✅ 这个是关键：FastAPI依赖注入用的 session getter
@asynccontextmanager
async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session

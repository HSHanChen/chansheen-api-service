import os

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional, Dict
from pathlib import Path
from dotenv import load_dotenv
import json

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

# 加载用户数据
def load_users() -> Dict[str, Dict[str, str]]:
    file_path = Path("app/data/users.json")
    if not file_path.exists():
        raise FileNotFoundError("用户数据文件不存在")
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)

# 校验用户
def verify_user(username: str, password: Optional[str] = None) -> Optional[Dict[str, str]]:
    users = load_users()
    user = users.get(username)
    if user and (password is None or user.get("password") == password):
        return {"username": username}
    return None

# 创建Token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 获取当前用户
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="无法验证的凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print("Decoded payload:", payload)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = verify_user(username, None)
    if user is None:
        raise credentials_exception
    return user









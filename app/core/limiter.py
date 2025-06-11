"""
@Author: Chan Sheen
@Date: 2025/6/11 11:40
@File: limiter.py
@Description: 
"""
# app/core/limiter.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)


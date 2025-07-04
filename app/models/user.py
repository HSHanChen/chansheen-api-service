"""
@Author: Chan Sheen
@Date: 2025/6/16 17:17
@File: user.py
@Description: 
"""
from pyasn1.type.univ import Boolean
# app/models/user.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column("UserName", String(50), unique=True, nullable=False, index=True)
    password = Column("Passwd", String(128), nullable=False)
    invalid = Column(Integer, nullable=True)

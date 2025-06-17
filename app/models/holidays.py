"""
@Author: Chan Sheen
@Date: 2025/6/17 09:40
@File: holidays.py
@Description: 
"""
from pyasn1.type.univ import Boolean
# app/models/user.py

from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Holidays(Base):
    __tablename__ = "Holidays"

    date = Column(Date, primary_key=True)
    dateType = Column(Integer, nullable=False)
    weekName = Column(String(10), nullable=False)
    note = Column("Note", String(50))
    lunar = Column("Lunar", String(20))

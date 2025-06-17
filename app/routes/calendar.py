import os
import json
import re
from fastapi import APIRouter, Query, HTTPException, Header, Depends
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.auth import get_current_user
from app.core.limiter import limiter
from fastapi import Request
from app.models.holidays import Holidays
from app.core.database import async_session, Base, get_async_session
from sqlalchemy import cast, String

router = APIRouter()
@router.get("/")
@limiter.limit("10/minute")
async def query_calendar(
        request: Request,
        year: str | None = Query(None),
        month: str | None = Query(None),
        date: str | None = Query(None),
        session: AsyncSession = Depends(get_async_session),
        current_user: dict = Depends(get_current_user)
):
    if year:
        key_prefix = year
        label = "年份"
        _ = int(year)
    elif month:
        key_prefix = month
        label = "月份"
        try:
            datetime.strptime(month, "%Y-%m")
            if not re.match(r"^\d{4}-\d{2}$", month):
                raise ValueError
        except ValueError:
            raise HTTPException(status_code=400, detail="月份格式错误，应为 YYYY-MM")
    elif date:
        key_prefix = date
        label = "日期"
        try:
            datetime.strptime(date, "%Y-%m-%d")
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
                raise ValueError
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式错误，应为 YYYY-MM-DD")

        stmt = select(Holidays).where(Holidays.date == date)
        result = await session.execute(stmt)
        holiday_info = result.scalar_one_or_none()

        if holiday_info:
            return {
                "date": str(holiday_info.date),
                "lunar": holiday_info.lunar,
                "dateType": holiday_info.dateType,
                "weekday": holiday_info.weekName,
                "note": holiday_info.note
            }
        else:
            raise HTTPException(status_code=200, detail=f"{date} 非节假日或调休")
    else:
        raise HTTPException(status_code=400, detail="必须提供：year, month 或 date 参数且只能一个")

    # year 或 month 查询
    stmt = select(Holidays).where(cast(Holidays.date, String).like(f"{key_prefix}%"))
    result = await session.execute(stmt)
    holiday_info = result.scalars().all()

    if not holiday_info:
        raise HTTPException(status_code=404, detail=f"{label} {key_prefix} 未维护节假日信息")

    return [{
        "date": str(h.date),
        "lunar": h.lunar,
        "dateType": h.dateType,
        "weekday": h.weekName,
        "note": h.note
    } for h in holiday_info]
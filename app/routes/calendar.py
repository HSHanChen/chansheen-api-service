import re

from fastapi import APIRouter, Query, HTTPException, Header, Depends
from datetime import datetime
from app.core.auth import get_current_user
from app.core.limiter import limiter
from fastapi import Request
import json
import os

router = APIRouter()

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "holiday_data.json")
with open(DATA_FILE, "r", encoding="utf-8") as f:
    HOLIDAYS = json.load(f)


@router.get("")
@limiter.limit("10/minute")
def query_calendar(
        request: Request,
        year: str | None = Query(None),
        month: str | None = Query(None),
        date: str | None = Query(None),
        current_user: dict = Depends(get_current_user)
):
    if year:
        key_prefix = year
        label = "年份"
        format_check = lambda x: int(x)
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
        holiday_info = HOLIDAYS.get(date)
        if holiday_info:
            return {
                "date": date,
                "lunar": holiday_info.get("lunar"),
                "dateType": holiday_info.get("dateType"),
                "weekday": holiday_info.get("weekName"),
                "note": holiday_info.get("note")
            }
        else:
            raise HTTPException(status_code=200, detail=f"{date} 非节假日或调休")
    else:
        raise HTTPException(status_code=400, detail="必须提供：year, month 或 date 参数且只能一个")

    results = []
    for d, info in HOLIDAYS.items():
        if d.startswith(key_prefix):
            results.append({
                "date": d,
                "lunar": info.get("lunar"),
                "dateType": info.get("dateType"),
                "weekday": info.get("weekName"),
                "note": info.get("note")
            })
    if not results:
        raise HTTPException(status_code=404, detail=f"{label} {key_prefix} 未维护节假日信息")
    return results

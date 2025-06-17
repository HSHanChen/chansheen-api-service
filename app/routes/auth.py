from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import verify_user, create_access_token
from app.core.database import async_session
from app.core.limiter import limiter

router = APIRouter()

@router.post("/token")
@limiter.limit("5/minute")
# async def login_for_access_token(
#     request: Request,
#     form_data: OAuth2PasswordRequestForm = Depends()
# ):
#     async with async_session() as session:
#         user = await verify_user(form_data.username, form_data.password, session)
#         if not user:
#             raise HTTPException(status_code=400, detail="用户名或密码错误")
#         access_token = create_access_token(data={"sub": user["username"]})
#         return {"access_token": access_token, "token_type": "bearer"}
async def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    try:
        async with async_session() as session:
            user = await verify_user(form_data.username, form_data.password, session)
            if not user:
                raise HTTPException(status_code=400, detail="用户名或密码错误")
            access_token = create_access_token(data={"sub": user["username"]})
            return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")
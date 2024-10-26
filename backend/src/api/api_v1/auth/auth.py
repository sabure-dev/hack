from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from core.database import get_session
from crud.user_crud import create_user_crud
from .helpers import create_access_token, create_refresh_token
from .schemas import TokenInfo
from .validation import validate_auth_user, get_current_token_payload, get_current_active_auth_user, \
    get_current_auth_user_for_refresh, get_current_active_auth_user_for_refresh
from ..users import schemas as user_schemas

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login")
async def auth_user(user: user_schemas.ValidateUser = Depends(validate_auth_user)):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    "/refresh",
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
def auth_refresh_jwt(
        user: user_schemas.ValidateUser = Depends(get_current_active_auth_user_for_refresh),
):
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token,
    )

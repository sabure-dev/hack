from fastapi import Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.database import get_session
from .helpers import (
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
)
from . import utils as auth_utils
from ..users.schemas import CreateUser, UserSchema, UserOut
from crud.user_crud import get_user, get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login/",
)


def get_current_token_payload(
        token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


def validate_token_type(
        payload: dict,
        token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}",
    )


async def get_user_by_token_sub(payload: dict, session: AsyncSession) -> UserOut:
    username: str | None = payload.get("sub")
    if user := await get_user_by_username(username=username, session=session):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    async def __call__(
            self,
            payload: dict = Depends(get_current_token_payload),
            session: AsyncSession = Depends(get_session),
    ):
        validate_token_type(payload, self.token_type)
        return await get_user_by_token_sub(payload=payload, session=session)


get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)


def get_current_active_auth_user_for_refresh(
        user: UserSchema = Depends(get_current_auth_user_for_refresh),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="inactive user",
    )


def get_current_active_auth_user(
        user: UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="inactive user",
    )


async def validate_auth_user(
        username: str = Form(),
        password: str = Form(),
        session: AsyncSession = Depends(get_session),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    if not (user := await get_user_by_username(username=username, session=session)):
        raise unauthed_exc

    if not auth_utils.validate_password(
            password=password,
            hashed_password=user.hashed_password,
    ):
        raise unauthed_exc

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user

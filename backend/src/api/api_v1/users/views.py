from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from core.database import get_session
from crud.user_crud import create_user_crud
from . import schemas as user_schemas

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("", response_model=user_schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: user_schemas.CreateUser, session: AsyncSession = Depends(get_session)):
    user = await create_user_crud(user_in=user, session=session)

    return user

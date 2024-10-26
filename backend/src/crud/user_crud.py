"""
Create
Read
Update
Delete
"""
import sqlalchemy
from fastapi import HTTPException
from sqlalchemy import select
from fastapi import status

from api.api_v1.users import schemas as user_schemas
from sqlalchemy.ext.asyncio import AsyncSession
from models import users as user_models
from api.api_v1.auth import utils as auth_utils


async def create_user_crud(user_in: user_schemas.CreateUser, session: AsyncSession) -> user_schemas.UserOut:
    """
    Creates a new user.

    Args:
        - user_in (user_schemas.CreateUser): The user to create.
        - session (AsyncSession): The database session to use.

    Returns:
        - user_schemas.UserOut: The created user.

    Raises:
        - None
    """
    try:

        hashed_password = auth_utils.hash_password(user_in.hashed_password)
        new_user = user_models.User(username=user_in.username,
                                    hashed_password=hashed_password)

        session.add(new_user)
        await session.commit()

        user_model = user_schemas.UserOut.model_validate(new_user)

        return user_model
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exists.")


async def get_user(user_id: int, session: AsyncSession) -> user_schemas.UserOut:
    query = select(user_models.User).where(user_models.User.id == user_id)
    response = await session.execute(query)
    user = response.scalars().first()

    return user


async def get_user_by_username(username: str, session: AsyncSession) -> user_schemas.UserOut:
    query = select(user_models.User).where(user_models.User.username == username)
    response = await session.execute(query)
    user = response.scalars().first()

    return user

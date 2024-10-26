import datetime
from typing import Annotated
from sqlalchemy import text, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from .roles import Role

created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    hashed_password: Mapped[bytes]
    active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[str] = mapped_column(ForeignKey("role.title"), default="participant")
    created_at: Mapped[created_at]

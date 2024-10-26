from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from .users import User


class Judge(Base):
    __tablename__ = "judge"

    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    username: Mapped[str] = mapped_column(ForeignKey("user.username"))

import datetime
from typing import Annotated
from sqlalchemy import text, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .users import User
from .teams import Team
from core.database import Base


class Participant(Base):
    __tablename__ = "participant"

    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    username: Mapped[str] = mapped_column(ForeignKey("user.username"))
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"), nullable=True, default=None)

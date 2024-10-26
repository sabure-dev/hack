from sqlalchemy import text, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime
from core.database import Base
from .teams import Team


class Match(Base):
    __tablename__ = "match"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime]
    team1: Mapped[int] = mapped_column(ForeignKey("team.id"))
    team2: Mapped[int] = mapped_column(ForeignKey("team.id"))
    winner_team_id: Mapped[int] = mapped_column(ForeignKey("team.id"), nullable=True, default=None)

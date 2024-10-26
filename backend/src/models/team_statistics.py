from sqlalchemy import text, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime
from matches import Match
from teams import Team
from core.database import Base


class TeamStatistics(Base):
    __tablename__ = "team_statistics"

    id: Mapped[int] = mapped_column(primary_key=True)

    total_games: Mapped[int] = mapped_column(default=0)
    total_wins: Mapped[int] = mapped_column(default=0)
    total_losses: Mapped[int] = mapped_column(default=0)
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))

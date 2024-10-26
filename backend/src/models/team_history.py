from sqlalchemy import text, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime
from matches import Match
from teams import Team
from core.database import Base


class TeamHistory(Base):
    __tablename__ = "team_history"

    id: Mapped[int] = mapped_column(primary_key=True)

    match_date: Mapped[datetime] = mapped_column(ForeignKey("match.date"))
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))

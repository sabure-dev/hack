from sqlalchemy import text, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .matches import Match
from .teams import Team
from .scores import Score
from core.database import Base


class Result(Base):
    __tablename__ = "result"

    id: Mapped[int] = mapped_column(primary_key=True)

    match_id: Mapped[int] = mapped_column(ForeignKey("match.id"))
    total_score: Mapped[int] = mapped_column(default=0)
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))

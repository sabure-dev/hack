from sqlalchemy import text, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime
from .matches import Match
from .judges import Judge
from .teams import Team
from core.database import Base


class Score(Base):
    __tablename__ = "score"

    id: Mapped[int] = mapped_column(primary_key=True)

    match_id: Mapped[int] = mapped_column(ForeignKey("match.id"))
    judge_id: Mapped[int] = mapped_column(ForeignKey("judge.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    score: Mapped[int] = mapped_column(default=0)

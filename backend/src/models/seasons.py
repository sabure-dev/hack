from sqlalchemy import text, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from .teams import Team


class Season(Base):
    __tablename__ = "season"

    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[str] = mapped_column(nullable=False)
    champion_team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))

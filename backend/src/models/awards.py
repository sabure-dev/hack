from sqlalchemy import text, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from .seasons import Season

from core.database import Base


class Award(Base):
    __tablename__ = "award"

    id: Mapped[int] = mapped_column(primary_key=True)
    award_name: Mapped[str] = mapped_column(nullable=False)
    season_id: Mapped[int] = mapped_column(ForeignKey("season.id"))

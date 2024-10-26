from typing import Annotated
from sqlalchemy import text, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base

year_type = Annotated[str, mapped_column(server_default=text("to_char((CURRENT_DATE), 'yyyy')"))]


class Team(Base):
    __tablename__ = "team"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    city: Mapped[str] = mapped_column(String(30))
    year_formed: Mapped[year_type]

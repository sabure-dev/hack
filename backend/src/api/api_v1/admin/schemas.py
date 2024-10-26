from pydantic import BaseModel


class TeamIn(BaseModel):
    title: str
    city: str
    year_formed: str

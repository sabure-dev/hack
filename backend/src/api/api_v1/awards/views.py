from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from models import awards

router = APIRouter(prefix="",
                   tags=["Awards"])


@router.get("/seasons/{season_id}/awards")
async def get_season_awards(
        season_id: int,
        session: AsyncSession = Depends(get_session)
):
    awards_q = await session.execute(select(awards.Award).where(awards.Award.season_id == season_id))
    awards_list = awards_q.scalars().all()
    return awards_list

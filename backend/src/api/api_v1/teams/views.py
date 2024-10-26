from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from models import awards, judges, seasons, scores, matches, users, participants, teams
from core.database import get_session
from api.api_v1.users import schemas as user_schemas
from typing import List
from api.api_v1.auth.validation import get_current_active_auth_user
from datetime import datetime

router = APIRouter(prefix="/teams",
                   tags=["Teams"])


@router.put("")
async def add_to_team(user_id: int, team_id: int,
                      current_user: user_schemas.UserOut = Depends(get_current_active_auth_user),
                      session: AsyncSession = Depends(get_session)):
    participant_q = await session.execute(
        select(participants.Participant).where(participants.Participant.id == current_user.id))
    participant = participant_q.scalars().first()

    if current_user.role != "admin" and participant.team_id != team_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You do not have permission to perform this action.")
    team_q = await session.execute(select(teams.Team).where(teams.Team.id == team_id))
    team = team_q.scalar_one_or_none()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    add_participant_q = await session.execute(
        select(participants.Participant).where(participants.Participant.id == user_id))

    participant = add_participant_q.scalars().first()

    if not participant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User to add not found")

    participant.team_id = team_id

    await session.commit()

    return participant

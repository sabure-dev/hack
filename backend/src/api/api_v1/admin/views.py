from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from models import awards, judges, seasons, scores, matches, users, participants
from core.database import get_session
from api.api_v1.users import schemas as user_schemas
from typing import List
from api.api_v1.auth.validation import get_current_active_auth_user
from datetime import datetime

router = APIRouter(prefix="/admin",
                   tags=["Admin"])


@router.put("/users/{user_id}/role", status_code=status.HTTP_200_OK)
async def update_user_role(
        user_id: int,
        new_role: str = "judge",
        current_user: user_schemas.UserOut = Depends(get_current_active_auth_user),
        session: AsyncSession = Depends(get_session)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update user roles")

    user_q = await session.execute(select(users.User).where(users.User.id == user_id))
    user = user_q.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role == new_role:
        raise HTTPException(status_code=403, detail="Role cannot be updated")

    user.role = new_role

    participant_q = await session.execute(
        select(participants.Participant).where(participants.Participant.id == user_id))

    participant = participant_q.scalar_one_or_none()
    if participant:
        await session.delete(participant)

    new_judge = judges.Judge(
        id=user.id,
        username=user.username
    )

    session.add(new_judge)

    await session.commit()

    return {"message": "User role updated successfully"}


@router.post("/matches", status_code=201)
async def create_match(
        date: datetime,
        team1_id: int,
        team2_id: int,
        current_user: user_schemas.UserOut = Depends(get_current_active_auth_user),
        session: AsyncSession = Depends(get_session)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update user roles")

    new_match = matches.Match(
        date=date,
        team1=team1_id,
        team2=team2_id
    )
    session.add(new_match)
    await session.commit()

    return {"message": "Match created successfully"}


@router.post("/seasons", status_code=201)
async def create_season(
        year: str,
        champion_team_id: int | None = None,
        current_user: user_schemas.UserOut = Depends(get_current_active_auth_user),
        session: AsyncSession = Depends(get_session)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update user roles")

    new_season = seasons.Season(
        year=year,
        champion_team_id=champion_team_id
    )
    session.add(new_season)
    await session.commit()

    return {"message": "Season created successfully"}


@router.post("/awards", status_code=201)
async def create_award(
        award_name: str,
        season_id: int,
        current_user: user_schemas.UserOut = Depends(get_current_active_auth_user),
        session: AsyncSession = Depends(get_session)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update user roles")

    new_award = awards.Award(
        award_name=award_name,
        season_id=season_id
    )
    session.add(new_award)
    await session.commit()

    return {"message": "Award created successfully"}


@router.get("/seasons/{season_id}/awards")
async def get_season_awards(
        season_id: int,
        session: AsyncSession = Depends(get_session)
):
    awards_q = await session.execute(select(awards.Award).where(awards.Award.season_id == season_id))
    awards_list = awards_q.scalars().all()
    return awards_list


@router.put("/season/winner")
async def select_champion(
        season_id: int,
        new_champion_team_id: int,
        current_user: user_schemas.UserOut = Depends(get_current_active_auth_user),
        session: AsyncSession = Depends(get_session),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    season_q = await session.execute(select(seasons.Season).where(seasons.Season.id == season_id))
    season = season_q.scalars().first()
    season.champion_team_id = new_champion_team_id

    await session.commit()
    return season


@router.put("/matches/winner")
async def select_match_winner(
        match_id: int,
        new_match_winner_team_id: int,
        current_user: user_schemas.UserOut = Depends(get_current_active_auth_user),
        session: AsyncSession = Depends(get_session),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    match_q = await session.execute(select(matches.Match).where(matches.Match.id == match_id))
    match = match_q.scalars().first()

    if (new_match_winner_team_id != match.team1) and (new_match_winner_team_id != match.team2):
        raise HTTPException(status_code=404,
                            detail=f"Team with id {new_match_winner_team_id} did not participate in match with id {match_id}")

    match.winner_team_id = new_match_winner_team_id

    await session.commit()

    return match

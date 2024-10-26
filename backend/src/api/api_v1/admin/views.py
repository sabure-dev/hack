from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status
from .schemas import TeamIn

from models import awards, judges, seasons, scores, matches, users, participants, teams, team_statistics, team_history
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

    team1_stats_q = await session.execute(
        select(team_statistics.TeamStatistics).where(team_statistics.TeamStatistics.team_id == team1_id))
    team1_stats = team1_stats_q.scalars().first()

    team2_stats_q = await session.execute(
        select(team_statistics.TeamStatistics).where(team_statistics.TeamStatistics.team_id == team2_id))
    team2_stats = team2_stats_q.scalars().first()

    team1_stats.total_losses = team1_stats.total_losses + 1
    team2_stats.total_losses = team2_stats.total_losses + 1

    team1_stats.total_games = team1_stats.total_games + 1
    team2_stats.total_games = team2_stats.total_games + 1

    new_team_history1 = team_history.TeamHistory(match_date=date, team_id=team1_id)
    new_team_history2 = team_history.TeamHistory(match_date=date, team_id=team2_id)

    session.add(new_match)
    session.add(new_team_history1)
    session.add(new_team_history2)
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

    team_stat_q = await session.execute(select(team_statistics.TeamStatistics).where(
        team_statistics.TeamStatistics.team_id == new_match_winner_team_id))
    team_stat = team_stat_q.scalars().first()
    team_stat.total_losses = team_stat.total_losses - 1
    team_stat.total_wins = team_stat.total_wins + 1

    await session.commit()

    return match


@router.post("/teams")
async def create_team(new_team: TeamIn, current_user: user_schemas.UserOut = Depends(get_current_active_auth_user),
                      session: AsyncSession = Depends(get_session)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    new_team_model = teams.Team(**new_team.model_dump())
    session.add(new_team_model)
    await session.commit()

    team_q = await session.execute(
        select(teams.Team).where(teams.Team.city == new_team.city, teams.Team.title == new_team.title,
                                 teams.Team.year_formed == new_team.year_formed))
    team = team_q.scalars().first()
    new_team_statistics = team_statistics.TeamStatistics(team_id=team.id)

    session.add(new_team_statistics)
    await session.commit()

    return new_team

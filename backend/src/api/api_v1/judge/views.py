from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.validation import get_current_active_auth_user
from core.database import get_session
from models.judges import Judge
from models.matches import Match
from models.scores import Score
from models.teams import Team
from models.results import Result
from ..users import schemas as user_schemas

router = APIRouter(
    prefix="/judge",
    tags=["Judge"],
)


@router.post("/scores", status_code=201)
async def score_team(
    match_id: int,
    team_id: int,
    score: int,
    current_user: user_schemas.UserOut = Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(get_session)
):

    match_q = await session.execute(select(Match).where(Match.id == match_id))
    match = match_q.scalars().first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    team_q = await session.execute(select(Team).where(Team.id == team_id))
    team = team_q.scalars().first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    if current_user.role != "judge":
        raise HTTPException(status_code=403, detail="Only judges can score teams")

    new_score = Score(
        match_id=match_id,
        judge_id=current_user.id,
        team_id=team_id,
        score=score
    )
    session.add(new_score)

    result_score_q = await session.execute(select(Result).where(Result.team_id == team_id))
    result_score = result_score_q.scalar_one_or_none()

    if result_score is None:
        new_result = Result(
            team_id=team_id,
            match_id=match_id,
            total_score=score,
        )

        session.add(new_result)

        await session.commit()
    else:
        result_score.total_score = result_score.total_score + score

        await session.commit()

    return {"message": "Team scored successfully"}


@router.get("/scores")
async def get_match_scores(
    match_id: int,
    session: AsyncSession = Depends(get_session)
):
    scores_q = await session.execute(select(Score).filter(Score.match_id == match_id))
    scores = scores_q.scalars().all()
    return scores

from fastapi import FastAPI
from api.api_v1.auth.auth import router as auth_router
from api.api_v1.users.views import router as users_router
from api.api_v1.judge.views import router as judge_router
from api.api_v1.admin.views import router as admin_router
from api.api_v1.teams.views import router as teams_router
from api.api_v1.awards.views import router as awards_router

app = FastAPI(title="HackWar")

app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(judge_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")
app.include_router(teams_router, prefix="/api/v1")
app.include_router(awards_router, prefix="/api/v1")

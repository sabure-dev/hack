from fastapi import FastAPI
from api.api_v1.auth.auth import router as auth_router
from api.api_v1.users.views import router as users_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")

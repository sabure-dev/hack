from pathlib import Path

from dotenv import load_dotenv
import os

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent.parent

load_dotenv()


class DbSettings(BaseModel):
    db_host: str = os.getenv("DB_HOST")
    db_port: str = os.getenv("DB_PORT")
    db_name: str = os.getenv("DB_NAME")
    db_user: str = os.getenv("DB_USER")
    db_pass: str = os.getenv("DB_PASS")

    test_db_host: str = os.environ.get("TEST_DB_HOST")
    test_db_port: str = os.environ.get("TEST_DB_PORT")
    test_db_name: str = os.environ.get("TEST_DB_NAME")
    test_db_user: str = os.environ.get("TEST_DB_USER")
    test_db_pass: str = os.environ.get("TEST_DB_PASS")


class AuthJWTSettings(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = os.environ.get("ALGORITHM")
    access_token_expire_minutes: int = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS")


class Settings(BaseSettings):
    db: DbSettings = DbSettings()

    auth_jwt: AuthJWTSettings = AuthJWTSettings()


settings = Settings()

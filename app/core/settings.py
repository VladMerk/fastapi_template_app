from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    DB_URL: str = f'sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3'
    DB_ECHO: bool = True


settings = Settings()

from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR: Path = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DB_URL: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    DB_ECHO: bool = True
    PRIVATE_KEY: str = (BASE_DIR.parent / "certs" / "jwt-private.pem").read_text()
    PUBLIC_KEY: str = (BASE_DIR.parent / "certs" / "jwt-public.pem").read_text()
    ALGORITHM: str = "RS256"
    EXPIRES_TOKEN: int = 30


settings = Settings()

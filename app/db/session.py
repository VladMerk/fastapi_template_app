from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.settings import settings
from app.db.base import Base

engine: AsyncEngine = create_async_engine(
    url=settings.DB_URL,
    echo=settings.DB_ECHO,
)


session_factory = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


async def session_dependencies() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session
        await session.close()

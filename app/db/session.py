from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.core.config import settings

# Create async SQLAlchemy engine with connection pool
async_engine = create_async_engine(
    settings.async_database_url,
    echo=False,
    connect_args={"ssl": "require"},
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)

# Factory for request-scoped async sessions
async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncIterator[AsyncSession]:
    """
    FastAPI dependency yielding a request-scoped AsyncSession.
    Automatically commits on success and rolls back on exception.
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

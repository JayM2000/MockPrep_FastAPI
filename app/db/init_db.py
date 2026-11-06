import asyncio
from sqlalchemy import text
from app.db.base import Base
from app.db.session import async_engine
import app.models.job  # noqa: F401


async def init_ai_schema() -> None:
    """
    Ensures the 'ai' schema exists and creates all FastAPI-owned tables.
    """
    print("[DB Init] Initializing FastAPI 'ai' schema...")
    async with async_engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS ai;"))
        await conn.run_sync(Base.metadata.create_all)
    print("[DB Init] 'ai' schema and tables initialized successfully.")


if __name__ == "__main__":
    asyncio.run(init_ai_schema())

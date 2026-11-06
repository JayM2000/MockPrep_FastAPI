import uuid
from datetime import datetime, timezone
import pytest
from sqlalchemy import pool, select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings
from app.models.job import AIJob


@pytest.fixture
def test_async_engine():
    """
    Creates an async engine using NullPool for test isolation.
    Prevents Windows proactor event loop reuse errors across test functions.
    """
    engine = create_async_engine(
        settings.async_database_url,
        poolclass=pool.NullPool,
        connect_args={"ssl": "require"},
    )
    yield engine


@pytest.mark.anyio
async def test_database_connection(test_async_engine) -> None:
    """Verify async database connection to Neon PostgreSQL."""
    async with test_async_engine.connect() as conn:
        result = await conn.execute(text("SELECT 1 AS healthy"))
        assert result.scalar() == 1


@pytest.mark.anyio
async def test_ai_job_crud_in_ai_schema(test_async_engine) -> None:
    """Verify CRUD operations on ai.ai_jobs table."""
    session_factory = async_sessionmaker(
        bind=test_async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    test_job_id = f"job_test_{uuid.uuid4().hex[:8]}"
    test_project_id = f"proj_test_{uuid.uuid4().hex[:8]}"

    # Create
    async with session_factory() as session:
        job = AIJob(
            id=test_job_id,
            project_id=test_project_id,
            status="queued",
            message="Test job for Phase 5 verification",
            estimated_duration_seconds=10,
            result={"model": "test", "tokens": 100},
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        session.add(job)
        await session.commit()

    # Read
    async with session_factory() as session:
        stmt = select(AIJob).where(AIJob.id == test_job_id)
        result = await session.execute(stmt)
        fetched = result.scalar_one_or_none()
        assert fetched is not None
        assert fetched.id == test_job_id
        assert fetched.project_id == test_project_id
        assert fetched.status == "queued"
        assert fetched.result == {"model": "test", "tokens": 100}

        # Update
        fetched.status = "completed"
        await session.commit()

    # Verify update
    async with session_factory() as session:
        stmt = select(AIJob).where(AIJob.id == test_job_id)
        result = await session.execute(stmt)
        updated = result.scalar_one_or_none()
        assert updated is not None
        assert updated.status == "completed"

        # Cleanup
        await session.delete(updated)
        await session.commit()

    # Confirm deleted
    async with session_factory() as session:
        stmt = select(AIJob).where(AIJob.id == test_job_id)
        result = await session.execute(stmt)
        assert result.scalar_one_or_none() is None

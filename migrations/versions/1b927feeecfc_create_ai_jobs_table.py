"""create ai_jobs table

Revision ID: 1b927feeecfc
Revises: 
Create Date: 2026-11-06 18:25:36.205781

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1b927feeecfc'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: ensure schema 'ai' exists and create 'ai_jobs' table."""
    op.execute("CREATE SCHEMA IF NOT EXISTS ai;")
    op.execute("""
    CREATE TABLE IF NOT EXISTS ai.ai_jobs (
        id VARCHAR(64) PRIMARY KEY,
        project_id VARCHAR(64) NOT NULL,
        status VARCHAR(32) NOT NULL DEFAULT 'queued',
        message TEXT,
        estimated_duration_seconds INTEGER NOT NULL DEFAULT 15,
        result JSONB,
        error TEXT,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """)
    op.execute("CREATE INDEX IF NOT EXISTS ix_ai_ai_jobs_project_id ON ai.ai_jobs (project_id);")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE IF EXISTS ai.ai_jobs;")

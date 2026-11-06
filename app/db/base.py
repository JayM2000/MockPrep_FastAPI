from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

# Define 'ai' as the default schema for all models inheriting from Base.
# This enforces the architectural boundary: FastAPI owns the 'ai' schema.
metadata_obj = MetaData(schema="ai")


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models in the FastAPI service.
    """

    metadata = metadata_obj

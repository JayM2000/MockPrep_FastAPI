from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings powered by Pydantic Settings.
    Automatically reads variables from the environment and falls back to .env.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ENVIRONMENT: str = "development"
    PROJECT_NAME: str = "MockPrep AI Service"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    INTERNAL_API_PREFIX: str = "/internal/v1"

    # Shared secret header token for Express -> FastAPI machine-to-machine communication
    INTERNAL_SERVICE_TOKEN: str = "mockprep-internal-secret-token-change-in-prod"

    # Database connection string (PostgreSQL / Neon)
    DATABASE_URL: str = (
        "postgresql+asyncpg://neondb_owner:npg_2UGQ8pKSuwej@ep-mute-queen-abfugb4p-pooler.eu-west-2.aws.neon.tech/neondb"
    )

    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # CORS origins permitted to call this service
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",  # Next.js frontend
        "http://localhost:4000",  # Express API
    ]

    @computed_field
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"

    @computed_field
    @property
    def async_database_url(self) -> str:
        """
        Normalizes database URL to ensure postgresql+asyncpg driver prefix.
        Strips query strings for clean engine connect_args usage.
        """
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://") and not url.startswith("postgresql+asyncpg://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)

        if "?" in url:
            url = url.split("?")[0]
        return url


settings = Settings()

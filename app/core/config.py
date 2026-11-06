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


settings = Settings()

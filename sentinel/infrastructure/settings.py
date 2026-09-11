from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    database_url: str = (
        "postgresql+asyncpg://sentinel:sentinel@localhost:5432/llm_sentinel"
    )

    model_config = SettingsConfigDict(
        env_prefix="SENTINEL_",
        env_file=".env",
        extra="ignore",
    )
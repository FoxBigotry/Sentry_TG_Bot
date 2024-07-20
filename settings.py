from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, ValidationError
from logs.logger import get_logger

logger = get_logger()


class Settings(BaseSettings):
    """
    Class for application settings, loading parameters from the environment file (.env).
    """
    model_config = SettingsConfigDict(env_file='.env')

    TG_KEY: str = Field(..., description="Telegram bot token")
    CHAT_ID: str = Field(..., description="Telegram chat ID")
    MONGO_URI: str = Field(..., description="URI for connecting to MongoDB")
    MONGO_DB_NAME: str = Field(..., description="MongoDB database name")
    SENTRY_AUTH_TOKEN: str = Field(..., description="Sentry token")
    ORGANIZATION_SLUG: str = Field(..., description="Sentry organization slug")


# Attempt to load settings and error handling
try:
    settings = Settings()
except ValidationError as e:
    logger.error(f"Error loading settings:\n{e}")
    raise


__all__ = ["settings"]

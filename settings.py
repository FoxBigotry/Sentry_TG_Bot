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
    CHAT_LINK: str = Field(..., description="Telegram chat link")
    SENTRY_AUTH_TOKEN: str = Field(..., description="Sentry token")
    ORGANIZATION_SLUG: str = Field(..., description="Sentry organization slug")
    NGROK_AUTHTOKEN: str = Field(..., description=" Authtoken ngrok")

    # Database settings
    DB_USER: str = Field(..., description="Database username")
    DB_PASSWORD: str = Field(..., description="Database password")
    DB_HOST: str = Field(..., description="Database host")
    DB_PORT: int = Field(..., description="Database port")
    DB_NAME: str = Field(..., description="Database name")

    @property
    def database_url(self) -> str:
        return f"postgres://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def tortoise_orm(self) -> dict:
        return {
            "connections": {"default": self.database_url},
            "apps": {
                "models": {
                    "models": ["database_sql.models", "aerich.models"],
                    "default_connection": "default",
                }
            }
        }


# Attempt to load settings and error handling
try:
    settings = Settings()
except ValidationError as e:
    logger.error(f"Error loading settings:\n{e}")
    raise


__all__ = ["settings"]

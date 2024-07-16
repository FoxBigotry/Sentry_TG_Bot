from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, ValidationError


class Settings(BaseSettings):
    """
    Класс настроек приложения, загружающий параметры из файла окружения (.env).
    """
    model_config = SettingsConfigDict(env_file='.env')

    TG_KEY: str = Field(..., description="Telegram bot token")
    CHAT_ID: str = Field(..., description="ID чата Telegram")
    MONGO_URI: str = Field(..., description="URI для подключения к MongoDB")
    MONGO_DB_NAME: str = Field(..., description="Имя базы данных MongoDB")


# Попытка загрузки настроек и обработка ошибок
try:
    settings = Settings()
except ValidationError as e:
    print(f"Ошибка при загрузке настроек:\n{e}")
    raise


__all__ = ["settings"]

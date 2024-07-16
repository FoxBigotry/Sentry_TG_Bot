from pydantic import BaseModel, Field
from typing import Optional


class ErrorModel(BaseModel):
    error_id: str = Field(..., description="Уникальный ид ошибки")
    project_name: Optional[str] = Field(None, description="Имя проекта")
    type_error: Optional[str] = Field(None, description="Тип ошибки")
    value_error: Optional[str] = Field(None, description="Значение ошибки")
    url_error: Optional[str] = Field(None, description="URL ошибки в Sentry")
    event_id: Optional[str] = Field(None, description="ИД эвента ошибки")
    datetime: Optional[str] = Field(None, description="время получения ошибки")
    topic_id: Optional[str] = Field(None, description="ID чата в супер группе Telegram")

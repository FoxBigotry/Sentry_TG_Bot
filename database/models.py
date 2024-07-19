from pydantic import BaseModel, Field
from typing import Optional


class ErrorModel(BaseModel):
    error_id: str = Field(..., description="Unique error ID")
    project_name: Optional[str] = Field(None, description="Project name")
    type_error: Optional[str] = Field(None, description="Error type")
    value_error: Optional[str] = Field(None, description="Error value")
    url_error: Optional[str] = Field(None, description="Sentry error URL")
    event_id: Optional[str] = Field(None, description="Event ID")
    datetime: Optional[str] = Field(None, description="Error timestamp")
    topic_id: Optional[str] = Field(None, description="Telegram supergroup chat ID")

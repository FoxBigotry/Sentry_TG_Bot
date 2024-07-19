import datetime
from pydantic import BaseModel
from typing import Optional, Dict, Any
from database.models import ErrorModel
from database.connect import MongoDBActions
from settings import settings
from bot.bot import create_topic_f


class SentryPayload(BaseModel):
    id: str
    url: str
    project_name: str
    event: Dict[str, Any]

    @property
    def metadata(self) -> Dict[str, Any]:
        return self.event.get('metadata', {})

    @property
    def type_error(self) -> str:
        return self.metadata.get('type', 'not received')

    @property
    def value_error(self) -> str:
        return self.metadata.get('value', 'not received')

    @property
    def event_id_error(self) -> str:
        return self.event.get('event_id', 'not received')


async def process_error_data(payload: SentryPayload, mongo_actions: MongoDBActions) -> tuple[str, Optional[str]]:
    """
        Processes the error data received from a Sentry webhook.

        This function extracts relevant information from the SentryPayload object,
        checks if the error already exists in the MongoDB collection, and if not, creates
        a new forum topic in Telegram for this error. It then saves the error details
        to the MongoDB collection and formats a message for sending to Telegram.

        Args:
            payload (SentryPayload): The payload object containing the error data from Sentry.
            mongo_actions (MongoDBActions): An instance of MongoDBActions used for database operations.

        Returns:
            tuple[str, Optional[str]]: A tuple containing the formatted error message and the ID of the
                                       created or existing Telegram topic.
    """
    id_error = payload.id
    url_error = payload.url
    project_name_error = payload.project_name
    type_error = payload.type_error
    value_error = payload.value_error
    event_id_error = payload.event_id_error

    error = await mongo_actions.get_error(id_error)
    if error:
        topic_id = error.get('topic_id')
    else:
        topic_id = await create_topic_f(settings.CHAT_ID, id_error, type_error)

    error_data = ErrorModel(
        error_id=id_error,
        project_name=project_name_error,
        type_error=type_error,
        value_error=value_error,
        url_error=url_error,
        event_id=event_id_error,
        datetime=str(datetime.datetime.now()),
        topic_id=str(topic_id)
    )

    await mongo_actions.save_error_data(error_data)

    full_message = (f"Error in Sentry!!\n"
                    f"Project: {project_name_error}\n"
                    f"Error: {type_error}: {value_error}\n"
                    f"{url_error}")

    return full_message, topic_id

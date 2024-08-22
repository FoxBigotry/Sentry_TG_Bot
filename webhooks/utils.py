import requests
import datetime
from pydantic import BaseModel
from typing import Optional, Dict, Any
from settings import settings
from bot.bot import create_topic_f
from logs.logger import get_logger
from database_sql.models import SQLErrorModel_T
from database_sql.connect import TortoiseDBActions

logger = get_logger()

SENTRY_API_URL = "https://sentry.io/api/0/organizations/{organization_id_or_slug}/issues/{issue_id}/"


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


async def process_error_data(payload: SentryPayload, db_actions: TortoiseDBActions) -> tuple[str, Optional[str]]:
    """
        Processes the error data received from a Sentry webhook.

        This function extracts relevant information from the SentryPayload object,
        checks if the error already exists in the MongoDB collection, and if not, creates
        a new forum topic in Telegram for this error. It then saves the error details
        to the MongoDB collection and formats a message for sending to Telegram.

        Args:
            payload (SentryPayload): The payload object containing the error data from Sentry.
            db_actions (TortoiseDBActions): An instance of TortoiseDBActions used for database operations.

        Returns:
            tuple[str, Optional[str]]: A tuple containing the formatted error message and the ID of the
                                       created or existing Telegram topic.
    """
    id_error = int(payload.id)
    url_error = payload.url
    project_name_error = payload.project_name
    type_error = payload.type_error
    value_error = payload.value_error
    event_id_error = payload.event_id_error

    error = await db_actions.get_error(id_error)

    if error:
        topic_id = error.topic_id
    else:
        topic_id = await create_topic_f(settings.CHAT_ID, str(id_error), type_error)

    error_data_sql = SQLErrorModel_T(
        error_id=id_error,
        project_name=project_name_error,
        type_error=type_error,
        value_error=value_error,
        url_error=url_error,
        event_id=event_id_error,
        datetime=datetime.datetime.now(),
        topic_id=topic_id
    )

    await db_actions.save_error_data(error_data_sql)

    full_message = (f"Error in Sentry!!\n"
                    f"Project: {project_name_error}\n"
                    f"Error: {type_error}: {value_error}\n"
                    f"{url_error}")

    return full_message, topic_id


async def update_sentry_issue(issue_id: str, status: str = "resolved") -> None:
    """
        Updates the status of a Sentry issue.

        This function sends a PUT request to the Sentry API to update the status of a specific issue.
        The status can be set to "resolved". The function uses an
        authentication token to authorize the request.

        Parameters:
            - issue_id (str): The unique identifier of the Sentry issue to be updated.
            - status (str): The new status to be set for the issue. Default is "resolved".
    """
    headers = {
        "Authorization": f"Bearer {settings.SENTRY_AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "status": status
    }
    url = SENTRY_API_URL.format(organization_id_or_slug=settings.ORGANIZATION_SLUG, issue_id=issue_id)

    try:
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        logger.debug(f"Successfully updated Sentry issue status:\nissue status to {status} for issue {issue_id}")
    except requests.RequestException as e:
        logger.error(f"Failed to update Sentry issue status: {e}")

import datetime
import logging
from fastapi import FastAPI, Request
from settings import settings
from aiogram.types import Update
from bot.bot import dp, bot, create_topic_f, send_telegram_message
from database.connect import MongoDBActions
from database.models import ErrorModel

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initializations
mongo_actions = MongoDBActions()


# Endpoint for handling Sentry webhooks
async def sentry_webhook(request: Request):
    payload = await request.json()
    event = payload.get('event')
    if event:
        id_error = payload.get('id', 'not received')
        url_error = payload.get('url', 'not received')
        project_name_error = payload.get('project_name', 'not received')
        meta = event.get('metadata', 'not received')
        type_error = meta.get('type', 'not received')
        value_error = meta.get('value', 'not received')
        event_id_error = event.get('event_id', 'not received')

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
        send_telegram_message(full_message, topic_id)

    return {"status": "received"}


# Endpoint for handling Telegram webhooks
async def telegram_webhook(request: Request):
    update = await request.json()
    telegram_update = Update(**update)
    await dp.feed_update(bot, telegram_update)
    return {"status": "ok"}

import logging
from fastapi import Request
from aiogram.types import Update
from bot.bot import dp, bot, send_telegram_message
from database.connect import MongoDBActions
from webhooks.utils import SentryPayload, process_error_data

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initializations
mongo_actions = MongoDBActions()


# Endpoint for handling Sentry webhooks
async def sentry_webhook(request: Request):
    try:
        payload_data = await request.json()
        payload = SentryPayload(**payload_data)
        full_message, topic_id = await process_error_data(payload, mongo_actions)

        send_telegram_message(full_message, topic_id)
        return {"status": "received"}
    except Exception as e:
        logger.error(f"Failed to process Sentry webhook: {e}")
        return {"status": "error", "message": str(e)}


# Endpoint for handling Telegram webhooks
async def telegram_webhook(request: Request):
    update = await request.json()
    telegram_update = Update(**update)
    await dp.feed_update(bot, telegram_update)
    return {"status": "ok"}

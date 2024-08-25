from fastapi import Request, APIRouter
from aiogram.types import Update
from bot.bot import dp, bot, send_telegram_message
from database_sql.connect import TortoiseDBActions
from webhooks.utils import SentryPayload, process_error_data, update_sentry_issue
from logs.logger import get_logger

# Logging
logger = get_logger()

# Initializations
db_actions = TortoiseDBActions()

router = APIRouter()


# Endpoint for handling Sentry webhooks
@router.post("/sentry-webhook")
async def sentry_webhook(request: Request):
    try:
        payload_data = await request.json()
        payload = SentryPayload(**payload_data)
        chat_link, full_message, topic_id = await process_error_data(payload, db_actions)

        send_telegram_message(chat_link, full_message, topic_id)
        await update_sentry_issue(issue_id=str(payload.id), status="resolved")
        return {"status": "received"}
    except Exception as e:
        logger.error(f"Failed to process Sentry webhook:\n{e}")
        return {"status": "error", "message": str(e)}


# Endpoint for handling Telegram webhooks
@router.post("/webhook/{settings.TG_KEY}")
async def telegram_webhook(request: Request):
    update = await request.json()
    telegram_update = Update(**update)
    await dp.feed_update(bot, telegram_update)
    return {"status": "ok"}

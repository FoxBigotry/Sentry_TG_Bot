import datetime
import requests
import logging
from fastapi import FastAPI, Request
from settings import settings
from aiogram.types import Update
from bot.bot import dp, bot, create_topic_f
from database.connect import MongoDBActions
from database.models import ErrorModel

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализации
app = FastAPI()
mongo_actions = MongoDBActions()

# Конфигурация для Telegram
TELEGRAM_TOKEN = settings.TG_KEY
CHAT_ID = settings.CHAT_ID
TELEGRAM_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'


# Функция для отправки сообщения в Telegram
def send_telegram_message(text, topic_id=None):
    payload = {
        'chat_id': CHAT_ID,
        'text': text
    }
    if topic_id:
        payload['message_thread_id'] = topic_id

    try:
        response = requests.post(TELEGRAM_URL, data=payload)
        response.raise_for_status()
        logging.debug(f"Успешная отправка сообщения в Telegram:\n{response.text}")
    except requests.RequestException as e:
        logging.error(f"Не удалось отправить сообщение в Telegram:\n{e}")


# Эндпоинт для обработки вебхуков от Sentry
@app.post("/sentry-webhook")
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
            topic_id = await create_topic_f(CHAT_ID, id_error, type_error)

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
        await mongo_actions.add_error(error_data)

        full_message = (f"Ошибка в Sentry!!\n"
                        f"Проект: {project_name_error}\n"
                        f"Ошибка: {type_error}: {value_error}\n"
                        f"{url_error}")
        send_telegram_message(full_message, topic_id)

    return {"status": "received"}


# Эндпоинт для обработки вебхуков от Telegram
@app.post(f"/webhook/{TELEGRAM_TOKEN}")
async def telegram_webhook(request: Request):
    update = await request.json()
    telegram_update = Update(**update)
    await dp.feed_update(bot, telegram_update)
    return {"status": "ok"}


# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

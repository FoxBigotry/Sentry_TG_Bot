import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from settings import settings
from logs.logger import get_logger

# Logging
logger = get_logger()

# Telegram Configuration
bot = Bot(token=settings.TG_KEY)
dp = Dispatcher()
TELEGRAM_URL = f'https://api.telegram.org/bot{settings.TG_KEY}/sendMessage'


def send_telegram_message(text, topic_id=None):
    """
    Function to send a message to Telegram
    """
    payload = {
        'chat_id': settings.CHAT_ID,
        'text': text
    }
    if topic_id:
        payload['message_thread_id'] = topic_id

    try:
        response = requests.post(TELEGRAM_URL, data=payload)
        response.raise_for_status()
        logger.debug(f"Successful message sent to Telegram:\n{response.text}")
    except requests.RequestException as e:
        logger.error(f"Failed to send message to Telegram:\n{e}")


async def create_topic_f(chat_id: int, id_e: str, type_e: str) -> int:
    """
    Creates a new topic (chat) in the Telegram supergroup and returns its ID.

    :param chat_id: The ID of the chat.
    :param id_e: The ID of the error.
    :param type_e: The type of error.
    :return: The ID of the created topic (chat).
    """
    topic_name = f"{id_e} {type_e}"

    try:
        topic = await bot.create_forum_topic(chat_id, name=topic_name)
        topic_id = topic.message_thread_id
        return topic_id
    except Exception as e:
        logger.error(f"Error creating topic:\n{e}")
        return None


@dp.message(CommandStart())
async def cmd_start(message: Message):
    """
    Handles the /start command.
    """
    await message.answer('Working')

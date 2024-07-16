from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from settings import settings

TELEGRAM_TOKEN = settings.TG_KEY

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


async def create_topic_f(chat_id: int, id_e: str, type_e: str) -> int:
    """
    Создает новый топик(чат) в супер группе Telegram и возвращает его ID.

    :param chat_id: ID чата.
    :param id_e: ID ошибки.
    :param type_e: Тип ошибки.
    :return: ID созданного топика(чата).
    """
    topic_name = f"{id_e} {type_e}"

    try:
        topic = await bot.create_forum_topic(chat_id, name=topic_name)
        topic_id = topic.message_thread_id
        return topic_id
    except Exception as e:
        print(f"Ошибка при создании топика:\n{e}")
        return None


@dp.message(CommandStart())
async def cmd_start(message: Message):
    """
    Обрабатывает команду /start.
    """
    await message.answer('работаю')

import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from typing import Optional, Dict, Any
from database.models import ErrorModel
from settings import settings


class MongoDBConnection:
    def __init__(self):
        self.cluster = AsyncIOMotorClient(settings.MONGO_URI)
        self.db = self.cluster[settings.MONGO_DB_NAME]


class MongoDBActions(MongoDBConnection):
    @property
    def error_collection(self) -> AsyncIOMotorCollection:
        return self.db["error"]

    error_model = ErrorModel

    async def add_error(self, error_data: ErrorModel) -> None:
        """
        Добавляет ошибку в коллекцию.
        """
        try:
            await self.error_collection.insert_one(error_data.dict())
        except Exception as e:
            logging.error(f"Ошибка при сохранение данных:\n {e}")

    async def get_error(self, error_id: str) -> Optional[Dict[str, Any]]:
        """
        Получает ошибку из коллекции по идентификатору.
        """
        try:
            error = await self.error_collection.find_one({'error_id': error_id})
            return error
        except Exception as e:
            logging.error(f"Ошибка при попытке достать данные:\n {e}")
            return None

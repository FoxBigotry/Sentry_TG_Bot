from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from typing import Optional, Dict, Any
from database.models import ErrorModel
from settings import settings
from logs.logger import get_logger

logger = get_logger()


class MongoDBConnection:
    def __init__(self):
        self.cluster = AsyncIOMotorClient(settings.MONGO_URI)
        self.db = self.cluster[settings.MONGO_DB_NAME]


class MongoDBActions(MongoDBConnection):
    @property
    def error_collection(self) -> AsyncIOMotorCollection:
        return self.db["error"]

    error_model = ErrorModel

    async def save_error_data(self, error_data: ErrorModel) -> None:
        """
        Adds an error to the collection.
        """
        try:
            await self.error_collection.insert_one(error_data.dict())
        except Exception as e:
            logger.error(f"Error while saving data:\n {e}")

    async def get_error(self, error_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves an error from the collection by its identifier.
        """
        try:
            error = await self.error_collection.find_one({'error_id': error_id})
            return error
        except Exception as e:
            logger.error(f"Error retrieving data:\n {e}")
            return None

from tortoise import Tortoise
from typing import Optional
from database_sql.models import SQLErrorModel, TG_Configuration
from settings import settings
from logs.logger import get_logger

logger = get_logger()


class TortoiseDBConnection:
    """
       Class for managing database connections using Tortoise ORM.

       This class provides methods for initializing the database connection, configuring
       Tortoise ORM, and generating the database schemas, as well as closing all active
       database connections.

       Methods:
           - connection: Initializes the database connection, configures Tortoise ORM,
             and generates the database schemas.
           - close_connections: Closes all active database connections.

       Usage Example:
           db_connection = TortoiseDBConnection()
           await db_connection.connection()
           # Perform database operations
           await db_connection.close_connections()
    """
    async def connection(self):
        """
                Initializes the database connection and generates the database schemas.

                This method configures Tortoise ORM based on the settings provided in
                `settings.TORTOISE_ORM`, and creates the necessary database schemas. In case
                of an initialization error, the error will be logged.

                Exceptions:
                    - Exception: Catches and logs any exceptions that occur during initialization.
        """
        logger.debug("Initializing Tortoise ORM")
        try:
            await Tortoise.init(config=settings.tortoise_orm)
            await Tortoise.generate_schemas()
            logger.debug("Tortoise ORM initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Tortoise ORM:\n{e}")

    async def close_connections(self):
        """
        Closes all active database connections.

        This method closes all connections that were opened by Tortoise ORM.
        In case of an error while closing connections, the error will be logged.

        Exceptions:
            - Exception: Catches and logs any exceptions that occur while closing connections.
        """
        logger.debug("Closing connections")
        try:
            await Tortoise.close_connections()
            logger.debug("Connections closed successfully")
        except Exception as e:
            logger.error(f"Error closing connections:\n{e}")


class TortoiseDBActions(TortoiseDBConnection):
    async def save_error_data(self, error_data: SQLErrorModel) -> None:
        """
        Adds an error to the collection.
        """
        try:
            await self.connection()
            data = error_data.__dict__.copy()
            data.pop('id', None)
            error = await SQLErrorModel.create(**data)
            logger.info(f"Added:\n{error}")
        except Exception as e:
            logger.error(f"Error while saving data:\n {e}")
        finally:
            await self.close_connections()

    async def get_error(self, error_id: int, chat_id: int) -> Optional[SQLErrorModel]:
        """
        Retrieves an error from the collection by its identifier.
        """
        try:
            await self.connection()
            error_data = await SQLErrorModel.filter(error_id=error_id, chat_id=chat_id).first()
            return error_data
        except Exception as e:
            logger.error(f"Error while retrieving data SQL:\n {e}")
            return None
        finally:
            await self.close_connections()

    async def save_chat_configuration(self, chat_data: TG_Configuration) -> Optional[int]:
        """
        Saves the chat configuration to the database.
        """
        try:
            await self.connection()
            chat_configuration = await TG_Configuration.create(tg_chat_id=chat_data.tg_chat_id,
                                                               tg_chat_link=chat_data.tg_chat_link)
            logger.info(f"Added:\n{chat_configuration}")
            return chat_configuration.chat_id
        except Exception as e:
            logger.error(f"Error while saving chat_data SQL:\n {e}")
            return None
        finally:
            await self.close_connections()

    async def get_chat_id(self, chat_link: str) -> Optional[TG_Configuration]:
        """
        Retrieves the chat configuration from the database by chat link.
        """
        try:
            await self.connection()
            chat_id = await TG_Configuration.filter(tg_chat_link=chat_link).first()
            return chat_id
        except Exception as e:
            logger.error(f"Error while retrieving chat data SQL:\n {e}")
            return None
        finally:
            await self.close_connections()

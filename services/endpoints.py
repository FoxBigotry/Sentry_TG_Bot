from fastapi import APIRouter
from pydantic import BaseModel
from database_sql.models import TG_Configuration
from database_sql.connect import TortoiseDBActions
from logs.logger import get_logger

logger = get_logger()
router = APIRouter()


# Define the data model for the POST request
class ProjectData(BaseModel):
    tg_chat_link: str
    project_name: str


db_actions = TortoiseDBActions()


@router.post("/add_link_project/")
async def add_link_project(data: ProjectData):
    try:
        chat_data = TG_Configuration(
            tg_chat_link=data.tg_chat_link,
            project_name=data.project_name
        )
        check_conf = await db_actions.get_chat_conf(chat_data)
        if check_conf:
            result = f"these settings already exist link_TG: {data.tg_chat_link} and project_name: {data.project_name}"
        else:
            result = f"settings added link_TG: {data.tg_chat_link} and project_name: {data.project_name}"
            await db_actions.save_chat_configuration(chat_data)
        return {"message": result}
    except Exception as e:
        logger.error(e)
        raise e


@router.get("/tg_configurations/")
async def get_tg_configurations():
    # await db_actions.connection()
    configurations = await TG_Configuration.all().values("tg_chat_link", "project_name")
    # await db_actions.close_connections()
    return configurations

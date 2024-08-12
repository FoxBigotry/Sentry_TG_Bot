import os
import sys
from pydantic import BaseModel
from pyngrok import ngrok
from dotenv import load_dotenv
from fastapi import FastAPI
from settings import settings
from webhooks.webhook import sentry_webhook, telegram_webhook
from logs.logger import get_logger
from database_sql.models import TG_Configuration
from database_sql.connect import TortoiseDBActions


load_dotenv()

# Logging
logger = get_logger()

# Initializations
app = FastAPI()

# Routes for webhooks
app.post("/sentry-webhook")(sentry_webhook)
app.post(f"/webhook/{settings.TG_KEY}")(telegram_webhook)


# Define the data model for the POST request
class InputData(BaseModel):
    tg_chat_link: str
    project_name: str


db_actions = TortoiseDBActions()


@app.post("/process-data/")
async def process_data(data: InputData):
    await db_actions.connection()
    chat_data = TG_Configuration(
        tg_chat_link=data.tg_chat_link,
        project_name=data.project_name
    )
    check_conf = await db_actions.get_chat_conf(chat_data)
    if check_conf:
        result = f"these settings already exist link_TG: {data.tg_chat_link} and project_name: {data.project_name}"
    else:
        result = f"settings added link_TG: {data.tg_chat_link} and project_name: {data.project_name}"
        await db_actions.save_chat_configuration_2(chat_data)
    await db_actions.close_connections()
    return {"message": result}


@app.get("/tg-configurations/")
async def get_tg_configurations():
    await db_actions.connection()
    configurations = await TG_Configuration.all().values("tg_chat_link", "project_name")
    await db_actions.close_connections()
    return configurations


def start_ngrok():
    """
    Starts an ngrok tunnel if the NGROK_AUTHTOKEN is set.
    Logs the public URL created by ngrok, or does nothing if the token is not set.
    """
    # Retrieve the ngrok token from the environment variables
    ngrok_authtoken = os.environ.get('NGROK_AUTHTOKEN')

    # Check if the token is set
    if ngrok_authtoken:
        # If a port is specified in the command line arguments, use it
        # Otherwise, the default port is 8000
        port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else "8000"

        # Connect to ngrok, creating a public URL for the specified port
        public_url = ngrok.connect(port).public_url
        logger.debug(f"ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:{port}\"")


# Application startup
if __name__ == "__main__":
    start_ngrok()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

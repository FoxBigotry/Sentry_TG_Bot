import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from webhooks.webhook import router as webhooks_router
from logs.logger import get_logger
from services.ngrok_start import start_ngrok
from services.endpoints import router as endpoints_router


load_dotenv()

# Logging
logger = get_logger()

# Initializations
app = FastAPI()


# Routes
app.include_router(webhooks_router)
app.include_router(endpoints_router)


# Application startup
if __name__ == "__main__":
    start_ngrok()
    uvicorn.run(app, host="0.0.0.0", port=8000)

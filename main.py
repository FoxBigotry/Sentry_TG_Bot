from dotenv import load_dotenv
from fastapi import FastAPI
from settings import settings
from webhooks.webhook import sentry_webhook, telegram_webhook
from logs.logger import get_logger
from services.ngrok_start import start_ngrok
from services.endpoints import router as endpoints_router


load_dotenv()

# Logging
logger = get_logger()

# Initializations
app = FastAPI()

# Routes for webhooks
app.post("/sentry-webhook")(sentry_webhook)
app.post(f"/webhook/{settings.TG_KEY}")(telegram_webhook)

app.include_router(endpoints_router)


# Application startup
if __name__ == "__main__":
    start_ngrok()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

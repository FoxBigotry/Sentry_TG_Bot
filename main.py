import logging
from fastapi import FastAPI
from settings import settings
from webhooks.webhook import sentry_webhook, telegram_webhook

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initializations
app = FastAPI()

# Routes for webhooks
app.post("/sentry-webhook")(sentry_webhook)
app.post(f"/webhook/{settings.TG_KEY}")(telegram_webhook)

# Application startup
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

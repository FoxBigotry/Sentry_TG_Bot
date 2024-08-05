import os
import sys
from pyngrok import ngrok
from dotenv import load_dotenv
from fastapi import FastAPI
from settings import settings
from webhooks.webhook import sentry_webhook, telegram_webhook
from logs.logger import get_logger

load_dotenv()

# Logging
logger = get_logger()

# Initializations
app = FastAPI()

# Routes for webhooks
app.post("/sentry-webhook")(sentry_webhook)
app.post(f"/webhook/{settings.TG_KEY}")(telegram_webhook)


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

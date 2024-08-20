import os
import sys
from pyngrok import ngrok
from logs.logger import get_logger

logger = get_logger()


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

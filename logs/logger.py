import logging
import sys
from logging import Logger


def create_handler(handler: logging.Handler) -> logging.Handler:
    """
    Configures a logging handler with a formatter.

    :param handler: Logging handler to configure.
    :return: Configured logging handler.
    """
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
    handler.setFormatter(formatter)
    return handler


def get_logger(name: str = __name__, log_file: str = "logfile.log", log_level: int = logging.DEBUG) -> Logger:
    """
    Configures and returns a logger.

    :param name: Name of the logger.
    :param log_file: File to log messages.
    :param log_level: Logging level.
    :return: Configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if not logger.handlers:
        # File handler
        fh_file = create_handler(logging.FileHandler(log_file, encoding='utf-8'))
        logger.addHandler(fh_file)

        # Console handler
        ch_console = create_handler(logging.StreamHandler(sys.stdout))
        logger.addHandler(ch_console)

    return logger

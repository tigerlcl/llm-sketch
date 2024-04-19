import sys
import logging


def setup_logger(level=logging.INFO):
    """Initialize a logger with console output."""
    logger = logging.getLogger()
    logger.setLevel(level)

    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(level)
    formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(message)s')
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    return logger

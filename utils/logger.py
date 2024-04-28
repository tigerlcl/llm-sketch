import sys
import logging


def setup_logger(fp):
    """Initialize a logger with console output."""
    logger = logging.getLogger()
    fhandler = logging.FileHandler(filename=fp, mode='w')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fhandler.setFormatter(formatter)
    logger.addHandler(fhandler)
    logger.setLevel(logging.INFO)

    return logger

import logging

import better_exceptions
import coloredlogs

coloredlogs.install(level='INFO')

def setup():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    return logger

LOGGER = setup()
INFO = LOGGER.info
WARN = LOGGER.warn
ERROR = LOGGER.error

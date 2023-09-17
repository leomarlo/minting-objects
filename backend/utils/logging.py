import os, sys
import logging

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def log(message):
    logging.debug(message)
    logging.info(message)
    logging.warning(message)
    logging.error(message)
    logging.critical(message)
    
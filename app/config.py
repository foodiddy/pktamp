import os
import logging
from logging.handlers import SysLogHandler

PCAP_DIR = "/var/lib/pktamp/pcaps"
MAX_UPLOAD_SIZE = 100 * 1024 * 1024

def setup_logging():
    logger = logging.getLogger("pktamp")
    logger.setLevel(logging.INFO)
    handler = SysLogHandler(address="/dev/log")
    formatter = logging.Formatter("%(name)s: %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = setup_logging()

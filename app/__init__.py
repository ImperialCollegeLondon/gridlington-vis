"""The main module for the Vis system."""

import logging
import logging.config
import os

from .log_config import logging_dict_config

logging.config.dictConfig(logging_dict_config)

log = logging.getLogger("api_logger")
log.debug("Logging is configured.")

LIVE_MODEL = os.environ.get("LIVE_MODEL", False)
log.debug("Using Live Model" if LIVE_MODEL else "Using Pre-Set Data")

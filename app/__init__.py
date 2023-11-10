"""The main module for the Vis system."""

import logging
import logging.config

from .log_config import logging_dict_config

logging.config.dictConfig(logging_dict_config)

log = logging.getLogger("api_logger")
log.debug("Logging is configured.")
log.info("Gridlington Visualisation System is running...")

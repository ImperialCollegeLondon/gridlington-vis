"""Dict configuration for formal logging."""

import os

LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "DEBUG")
FORMAT: str = "[%(levelname)s] %(asctime)s | %(message)s"
logging_dict_config = {
    "version": 1,
    "formatters": {
        "default": {
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": "None",
        },
        "basic": {
            "format": FORMAT,
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "console": {
            "formatter": "basic",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "level": LOG_LEVEL,
        },
        "file": {
            "level": LOG_LEVEL,
            "class": "logging.FileHandler",
            "filename": "./logs/logging_file.log",
            "formatter": "basic",
        },
    },
    "loggers": {
        "gunicorn": {"handlers": ["default", "file"], "level": "INFO"},
        "api_logger": {
            "handlers": ["console", "file"],
            "level": LOG_LEVEL,
        },
    },
}

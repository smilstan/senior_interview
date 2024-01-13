import logging
import os
import sys

from datetime import datetime
from logging import config


log_path = "logs"
os.makedirs(log_path, mode=0o777, exist_ok=True)
logging_start = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file_name = f"{logging_start}.log"
log_file_path = os.path.join(log_path, log_file_name)

logging_level = logging.DEBUG

logging_config = {
    'version': 1,
    'formatters': {
        'log_format': {
            'format': "%(asctime)s | %(levelname)-7s | %(name)-10s | %(lineno)-3d | %(filename)-25s | %(message)s"
        }
    },
    'handlers': {
        'console': {
            'class': "logging.StreamHandler",
            'formatter': "log_format",
            'stream': sys.stdout
        },
        'file': {
            'class': "logging.handlers.RotatingFileHandler",
            'formatter': "log_format",
            'filename': log_file_path,
            'mode': 'a',
            'maxBytes': 15 * 1024 * 1024,
            'level': logging_level
        }
    },
    'loggers': {
        'app': {
            'handlers': ["console", "file"]
        },
        'connector': {
            'handlers': ["console", "file"]
        },
    }
}

# configure logging
config.dictConfig(logging_config)

app_logger = logging.getLogger("app")
app_logger.setLevel(logging_level)
connector_logger = logging.getLogger("connector")
connector_logger.setLevel(logging_level)

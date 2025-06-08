#----------------------------------------------------------------------
# log_config.py
#
# Logging configuration for log management.
#----------------------------------------------------------------------

# Standard library imports - built-in modules that come with Python
import logging
import os
from datetime import datetime

# create the logs directory if not exists
LOG_DIR = os.path.join ("..","log")
os.makedirs(LOG_DIR, exist_ok=True)

# create the log file with current datetime
LOG_FILE = os.path.join(LOG_DIR, f"WikiBooks_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log" )

# configure the logger
logger = logging.getLogger("wikibooks_logger")

# Set global logging level to DEBUG (capture all messages DEBUG and above)
logger.setLevel(logging.DEBUG) 

# Define the log messages format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# file handler
file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

# Console handler: only WARNING and above will be shown on terminal
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.WARNING)

# Add handlers to the logger if they are not already added
if not logger.handlers:
    logger.addHandler(file_handler)
    # logger.addHandler(console_handler)


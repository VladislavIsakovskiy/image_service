import os

from dotenv import load_dotenv

from loguru import logger

load_dotenv()

LOG_FOLDER = os.environ.get("LOGS_FOLDER_ROOT")
LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL")

if LOGGING_LEVEL in ["DEBUG", "TRACE"]:
    logger.add(f"{LOG_FOLDER}/debug.log", format="{time} {level} {message}", level=LOGGING_LEVEL, rotation="5 MB",
               backtrace=True, diagnose=True)
else:
    logger.add(f"{LOG_FOLDER}/debug.log", format="{time} {level} {message}", level=LOGGING_LEVEL, rotation="5 MB")

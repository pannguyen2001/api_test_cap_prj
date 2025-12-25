import sys
from loguru import logger
from configs.constants import log_file_path

logger.remove()

logger.add(
    sys.stdout,
    colorize=True,
    format="<level>[{level}]</level>[<green>{time:YYYY-MM-DD HH:mm:ss}</green>][<cyan>{name}:{function}:{line}</cyan>] <level>{message}</level>",
)

logger.add(
    log_file_path,
    colorize=False,
    format="<level>[{level}]</level>[<green>{time:YYYY-MM-DD HH:mm:ss}</green>][<cyan>{name}:{function}:{line}</cyan>] <level>{message}</level>",
)
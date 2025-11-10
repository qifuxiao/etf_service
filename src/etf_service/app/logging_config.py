# src/logging_config.py
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
setup_logging()
# 可创建全局 logger
logger = logging.getLogger("etf_service")
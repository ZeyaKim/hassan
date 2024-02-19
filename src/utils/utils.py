"""
Util 기능을 모아놓은 모듈.
"""

import __main__
import logging
import os
from logging.handlers import RotatingFileHandler


def get_root_dir():
    root_dir = os.path.dirname(os.path.abspath(__main__.__file__))
    return root_dir


def init_logger(root_dir: str):
    log_dir = os.path.join(root_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("hassan")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)

    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "hassan.log"),
        encoding="utf-8",
        maxBytes=1024 * 1024,
        backupCount=2,
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.info("Logger initialized")

    return logger

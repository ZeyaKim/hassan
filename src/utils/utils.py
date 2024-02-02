"""
Util 기능을 모아놓은 모듈.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

import toml


def get_root_dir():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.dirname(current_dir)
    root_dir = os.path.dirname(src_dir)

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
        maxBytes=1024 * 1024, backupCount=2
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.info("Logger initialized")

    return logger


def load_config(root_dir: str):
    config_path = os.path.join(root_dir, "config.toml")
    with open(config_path, "r") as f:
        config = toml.load(f)
    return config

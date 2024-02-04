import logging
import os

from PySide6.QtGui import QStandardItemModel


class HassanTask(QStandardItemModel):
    def __init__(
        self,
        logger: logging.Logger,
        root_dir: str,
        audio_extractor,
        translator,
        subtitle_generator,
        file_path: str,
        settings: dict,
    ):
        super().__init__()
        self.logger = logger
        self.file_path = file_path
        self.parent_dir = os.path.dirname(file_path)

    def execute(self):
        self.logger.debug(f"execute: {self.file_path}")

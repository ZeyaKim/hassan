import logging
import os

from PySide6.QtCore import QStandardItemModel


class HassanTask(QStandardItemModel):
    def __init__(
        self,
        logger: logging.Logger,
        root_dir: str,
        audio_path: str,
        audio_extractor,
        translator,
        subtitle_generator,
    ):
        super().__init__()
        self.path = audio_path
        self.parent_dir = os.path.dirname(audio_path)

    def __dict__(self):
        pass

    # TODO: 작업을 시작한다. (실제로는 쓰레드를 생성하고, 쓰레드에서 작업을 시작한다.)
    def run(self):
        pass

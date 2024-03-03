from PyQt5.QtWidgets import QApplication
from src.gui.main_window import MainWindow
import sys
import os
import pathlib
import logging
import logging.handlers
from src.services.paths_storage import PathsStorage
from src.services.audio_extractor import AudioExtractor
from src.services.translator import Translator
from src.services.subtitle_generator import SubtitleGenerator
from src.services.process_handler import ProcessHandler

main_path = __file__
root_dir = os.environ["ROOT_DIR"] = str(pathlib.Path(main_path).parent.absolute())


def start_app():
    paths_storage = PathsStorage()
    audio_extractor = AudioExtractor()
    translator = Translator()
    subtitle_generator = SubtitleGenerator()

    process_handler = ProcessHandler(
        paths_storage,
        audio_extractor,
        translator,
        subtitle_generator,
    )

    app = QApplication(sys.argv)
    window = MainWindow(paths_storage, process_handler)
    window.show()
    sys.exit(app.exec())


def init_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    root_dir = os.environ["ROOT_DIR"]
    log_path = pathlib.Path(root_dir) / "logs" / "app.log"

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    rotating_file_handler = logging.handlers.RotatingFileHandler(  # 수정된 부분
        log_path, maxBytes=1024 * 1024 * 10, backupCount=5
    )

    rotating_file_handler.setLevel(logging.WARNING)  # 수정된 부분
    rotating_file_handler.setFormatter(formatter)

    logger.addHandler(rotating_file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)

    logger.info("Logging initialized")


if __name__ == "__main__":
    init_logging()
    start_app()

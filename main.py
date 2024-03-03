from PyQt5.QtWidgets import QApplication
from src.gui.main_window import MainWindow
import sys
import os
import pathlib
import logging
import logging.handlers

main_path = __file__
root_dir = os.environ["ROOT_DIR"] = str(pathlib.Path(main_path).parent.absolute())


def start_app():
    app = QApplication(sys.argv)
    window = MainWindow()
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

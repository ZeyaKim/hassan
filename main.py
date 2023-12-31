import logging
import os
import sys

from PySide6.QtWidgets import QApplication

from src.ui.main_window import MainWindow


def init_logger():
    os.makedirs("logs", exist_ok=True)

    # 로거 생성 및 레벨 설정
    logger = logging.getLogger("root")
    logger.setLevel(logging.INFO)

    # 콘솔 핸들러 생성 및 설정
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "%(asctime)s :: %(levelname)s :: %(module)s :: %(lineno)s :: %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)

    # 파일 핸들러 생성 및 설정
    file_handler = logging.FileHandler("logs/error.log")
    file_handler.setLevel(logging.ERROR)
    file_formatter = logging.Formatter(
        "%(asctime)s :: %(levelname)s :: %(module)s :: %(lineno)s :: %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)

    # 로거에 핸들러 추가
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.info("Logger initialized")

if __name__ == "__main__":
    init_logger()
    app = QApplication(sys.argv)

    # 기본적인 윈도우 (QWidget) 생성
    window = MainWindow()
    window.show()
    # 이벤트 루프 실행
    sys.exit(app.exec())

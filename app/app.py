import logging
from logging.handlers import RotatingFileHandler
import os
import sys

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from PySide6.QtWidgets import QApplication, QMainWindow


def init_logger():
    logger = logging.getLogger("hassan")
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)

    file_handler = RotatingFileHandler(
        os.path.join("logs", "hassan.log"), maxBytes=1024 * 1024, backupCount=2
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    logger.debug("Logger initialized")

    return logger


class Container(containers.DeclarativeContainer):
    logger = providers.Singleton(init_logger)


@inject
def main(logger: logging.Logger = Provide[Container.logger]) -> None:
    logger.info("Starting application")

    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("PySide6 Example")
    window.setGeometry(100, 100, 800, 600)

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])
    main()

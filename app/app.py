import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
import toml
from PySide6.QtWidgets import QApplication
from widgets.main_window import MainWindow

cur_dir = os.path.dirname(__file__)
root_dir = os.path.dirname(cur_dir)


def init_logger():
    log_dir = os.path.join(root_dir, "logs")
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    logger = logging.getLogger("hassan")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)

    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "hassan.log"), maxBytes=1024 * 1024, backupCount=2
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.debug("Logger initialized")

    return logger


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    config_toml = toml.load(os.path.join(root_dir, "config.toml"))
    config_toml["root_dir"] = root_dir
    config.from_dict(config_toml)

    logger = providers.Singleton(init_logger)


@inject
def main(
    logger: logging.Logger = Provide[Container.logger],
    root_dir: str = Provide[Container.config.root_dir],
) -> None:
    logger.info("Starting application")

    app = QApplication(sys.argv)

    window = MainWindow(logger, root_dir)
    window.setWindowTitle("PySide6 Example")
    window.setGeometry(100, 100, 800, 600)

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])
    main()

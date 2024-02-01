import logging
import sys

from dependency_injector.wiring import Provide, inject
from PySide6.QtWidgets import QApplication, QMainWindow

from utils.container import Container
from utils import utils


@inject
def main(
    app: QApplication = Provide[Container.app],
    logger: logging.Logger = Provide[Container.logger],
    main_window: QMainWindow = Provide[Container.main_window],
) -> None:

    logger.info("Starting application")

    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    container = Container()
    root_dir = container.root_dir()
    container.config.from_dict(utils.load_config(root_dir))
    container.wire(modules=[__name__])
    main()

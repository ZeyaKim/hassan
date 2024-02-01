import logging
import sys

from dependency_injector import wiring
from PySide6 import QtWidgets

from utils import container, utils


def main():
    app_container = container.Container()

    root_dir = app_container.root_dir()
    app_container.config.from_dict(utils.load_config(root_dir))
    app_container.wire(modules=[__name__])

    run_application()


@wiring.inject
def run_application(
    app: QtWidgets.QApplication = wiring.Provide[container.Container.app],
    logger: logging.Logger = wiring.Provide[container.Container.logger],
    main_window: QtWidgets.QMainWindow = wiring.Provide[
        container.Container.main_window
    ],
):
    logger.info("Starting application")
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

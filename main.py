import logging
import sys

from dependency_injector import wiring
from PySide6 import QtWidgets

from src.utils import container


def main():
    app_container = container.Container()

    config_manager = app_container.config_manager_provider()

    app_container.config_provider.from_dict(config_manager.load_config())
    app_container.wire(modules=[__name__])

    run_application()


@wiring.inject
def run_application(
    app: QtWidgets.QApplication = wiring.Provide[container.Container.app_provider],
    logger: logging.Logger = wiring.Provide[container.Container.logger_provider],
    main_window: QtWidgets.QMainWindow = wiring.Provide[
        container.Container.main_window_provider
    ],
):
    logger.info("Starting application")
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

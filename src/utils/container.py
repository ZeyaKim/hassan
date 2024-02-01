from dependency_injector import containers, providers

from PySide6.QtWidgets import QApplication

from utils import utils
from widgets.main_window import MainWindow
from widgets.path_panel import PathPanel
from widgets.settings_panel import SettingsPanel
from widgets.task_runner_panel import TaskRunnerPanel


class Container(containers.DeclarativeContainer):
    root_dir = providers.Callable(utils.get_root_dir)

    config = providers.Configuration()

    logger = providers.Singleton(utils.init_logger, root_dir)

    # model

    # service

    # ui
    app = providers.Singleton(QApplication)
    
    path_panel = providers.Factory(PathPanel, logger, root_dir)
    settings_panel = providers.Factory(SettingsPanel, logger, root_dir)
    task_runner_panel = providers.Factory(TaskRunnerPanel, logger, root_dir)

    main_window = providers.Factory(
        MainWindow,
        logger,
        root_dir,
        path_panel,
        settings_panel,
        task_runner_panel,
    )
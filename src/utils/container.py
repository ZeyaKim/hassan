from dependency_injector import containers, providers
from PySide6.QtWidgets import QApplication

from services import audio_extractor, subtitle_generator, translator
from services.task_runner import TaskRunner
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

    audio_extractor = providers.Singleton(
        audio_extractor.AudioExtractor, logger, root_dir
    )
    translator = providers.Singleton(translator.Translator, logger, root_dir)
    subtitle_generator = providers.Singleton(
        subtitle_generator.SubtitleGenerator, logger, root_dir
    )
    task_runner = providers.Singleton(
        TaskRunner,
        logger,
        root_dir,
        audio_extractor,
        translator,
        subtitle_generator,
    )

    # ui
    app = providers.Singleton(QApplication)

    path_panel = providers.Factory(PathPanel, logger, root_dir)
    settings_panel = providers.Factory(SettingsPanel, logger, root_dir)
    task_runner_panel = providers.Factory(
        TaskRunnerPanel, logger, root_dir, task_runner
    )

    main_window = providers.Factory(
        MainWindow,
        logger,
        root_dir,
        path_panel,
        settings_panel,
        task_runner_panel,
    )

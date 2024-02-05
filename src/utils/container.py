import logging

from dependency_injector import containers, providers
from PySide6.QtWidgets import QApplication

from src.services import audio_extractor, subtitle_generator, task_runner, translator
from src.utils import config_manager, utils
from src.widgets.main_window import MainWindow
from src.widgets.path_panel import PathPanel
from src.widgets.path_viewer import PathViewer
from src.widgets.settings_panel import SettingsPanel
from src.widgets.task_runner_panel import TaskRunnerPanel


class Container(containers.DeclarativeContainer):
    """
    Container class for managing dependencies and providing instances of various services and UI components.
    """

    root_dir_provider: providers.Provider[str] = providers.Singleton(utils.get_root_dir)

    logger_provider: providers.Provider[logging.Logger] = providers.Singleton(
        utils.init_logger, root_dir_provider
    )

    config_manager_provider: providers.Provider[config_manager.ConfigManager] = (
        providers.Singleton(
            config_manager.ConfigManager, logger_provider, root_dir_provider
        )
    )

    config_provider: providers.Configuration = providers.Configuration()

    path_viewer_provider: providers.Provider[PathViewer] = providers.Singleton(
        PathViewer, logger_provider
    )

    # services
    audio_extractor_provider: providers.Provider[audio_extractor.AudioExtractor] = (
        providers.Singleton(
            audio_extractor.AudioExtractor,
            logger_provider,
            root_dir_provider,
            config_manager_provider,
            config_provider,
        )
    )
    translator_provider: providers.Provider[translator.Translator] = (
        providers.Singleton(
            translator.Translator,
            logger_provider,
            root_dir_provider,
            config_manager_provider,
            config_provider,
        )
    )

    subtitle_generator_provider: providers.Provider[
        subtitle_generator.SubtitleGenerator
    ] = providers.Singleton(
        subtitle_generator.SubtitleGenerator,
        logger_provider,
        root_dir_provider,
        config_manager_provider,
        config_provider,
    )

    task_runner_provider: providers.Provider[task_runner.TaskRunner] = (
        providers.Singleton(
            task_runner.TaskRunner,
            logger_provider,
            root_dir_provider,
            audio_extractor_provider,
            translator_provider,
            subtitle_generator_provider,
            path_viewer_provider,
            config_provider,
        )
    )

    app_provider: providers.Provider[QApplication] = providers.Singleton(QApplication)

    path_panel_provider: providers.Provider[PathPanel] = providers.Factory(
        PathPanel, logger_provider, root_dir_provider, path_viewer_provider
    )
    settings_panel_provider: providers.Provider[SettingsPanel] = providers.Factory(
        SettingsPanel,
        logger_provider,
        root_dir_provider,
        audio_extractor_provider,
        translator_provider,
        subtitle_generator_provider,
        config_provider,
    )
    task_runner_panel_provider: providers.Provider[TaskRunnerPanel] = providers.Factory(
        TaskRunnerPanel, logger_provider, root_dir_provider, task_runner_provider
    )

    main_window_provider: providers.Provider[MainWindow] = providers.Factory(
        MainWindow,
        logger_provider,
        root_dir_provider,
        path_panel_provider,
        settings_panel_provider,
        task_runner_panel_provider,
    )

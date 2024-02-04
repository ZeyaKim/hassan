import logging

from dependency_injector import providers

from src.utils import config_manager
from src.utils.enums import SubtitleExtEnum


class SubtitleGenerator:
    """Class for subtitle generator service."""

    def __init__(
        self,
        logger: logging.Logger,
        root_dir: str,
        config_manager: config_manager.ConfigManager,
        config: providers.Configuration,
    ) -> None:
        """ """
        self.logger = logger
        self.root_dir = root_dir
        self.config_manager = config_manager
        self.config = config

    def change_subtitle_ext(self, subtitle_ext_enum: SubtitleExtEnum) -> None:
        """
        Change the subtitle extension in the configuration file.

        Args:
            subtitle_ext_enum (SubtitleExtEnum): The new subtitle extension.
        """
        config_map = self.config_manager.load_config()
        config_map["subtitle_generator"]["ext"] = subtitle_ext_enum.value

        config_provider = providers.Configuration()
        config_provider.from_dict(config_map)
        self.config.override(config_provider)

        self.config_manager.save_config(config_map)
        self.logger.info(
            f"Subtitle extension has been changed to {subtitle_ext_enum.value}"
        )

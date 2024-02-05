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
        self.config["subtitle_generator"]["subtitle_ext"] = subtitle_ext_enum.value
        self.config_manager.save_config(self.config)
        self.logger.info(
            f"Subtitle extension has been changed to {subtitle_ext_enum.value}"
        )
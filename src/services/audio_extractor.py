import logging

from src.utils import config_manager
from src.utils.enums import WhisperDeviceEnum, WhisperModelEnum


class AudioExtractor:
    """Class for audio extractor service."""

    def __init__(
        self,
        logger: logging.Logger,
        root_dir: str,
        config_manager: config_manager.ConfigManager,
        config: dict,
    ):
        self.logger = logger
        self.root_dir = root_dir
        self.config_manager = config_manager
        self.config = config

    def change_whisper_model(self, whisper_model_enum: WhisperModelEnum) -> None:
        self.config["audio_extractor"]["whisper_model"] = whisper_model_enum.value
        self.config_manager.save_config(self.config)
        self.logger.info(
            f"Whisper model has been changed to {whisper_model_enum.value}"
        )

    def change_whisper_device(self, whisper_device_enum: WhisperDeviceEnum) -> None:
        self.config["audio_extractor"]["device"] = whisper_device_enum.value
        self.config_manager.save_config(self.config)
        self.logger.info(
            f"Whisper device has been changed to {whisper_device_enum.value}"
        )

    def extract_audio(
        self, file_path: str, parent_dir: str, name: str, execution_settings: dict
    ) -> list:

        description: list = []

        # TODO: Implement audio extraction

        self.logger.info(f"{name} has been extracted successfully.")

        return description

from dependency_injector import providers

from src.utils.enums import WhisperModelEnum


class AudioExtractor:
    """Class for audio extractor service."""

    def __init__(self, logger, root_dir, config_manager, config):
        self.logger = logger
        self.root_dir = root_dir
        self.config_manager = config_manager
        self.config = config

    def change_whisper_model(self, whisper_model_enum: WhisperModelEnum) -> None:
        """
        Change the whisper model in the configuration file.

        Args:
            subtitle_ext_enum (WhisperModelEnum): The new whisper model.
        """
        config_map = self.config_manager.load_config()
        config_map["audio_extractor"]["whisper_model"] = whisper_model_enum.value

        config_provider = providers.Configuration()
        config_provider.from_dict(config_map)
        self.config.override(config_provider)

        self.config_manager.save_config(config_map)
        self.logger.info(
            f"Whisper model has been changed to {whisper_model_enum.value}"
        )

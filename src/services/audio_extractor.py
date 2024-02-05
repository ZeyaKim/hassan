
from src.utils.enums import WhisperModelEnum, WhisperDeviceEnum


class AudioExtractor:
    """Class for audio extractor service."""

    def __init__(self, logger, root_dir, config_manager, config):
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
        self.logger.info(f"Whisper device has been changed to {whisper_device_enum.value}")

    def extract_audio(self, path: str, name: str) -> None:
        self.logger.info(f"Extracting audio from {name}")
        
        description = []
        
        # TODO: Implement audio extraction
        
        self.logger.info(f"{name} has been extracted successfully.")
        
        return description
import logging
import os

import whisper

from src.utils import config_manager
from src.utils.enums import WhisperDeviceEnum, WhisperModelEnum
from src.utils.types import Sentence


class AudioExtractor:
    """
    A class that extracts audio transcriptions using the Whisper ASR model.

    Args:
        logger (logging.Logger): The logger object for logging messages.
        root_dir (str): The root directory of the project.
        config_manager (config_manager.ConfigManager): The configuration manager object.
        config (dict): The configuration dictionary.

    Attributes:
        logger (logging.Logger): The logger object for logging messages.
        root_dir (str): The root directory of the project.
        config_manager (config_manager.ConfigManager): The configuration manager object.
        config (dict): The configuration dictionary.
        model (whisper.Whisper | None): The Whisper ASR model.
        last_settings_info (dict | None): The last used audio extractor settings.

    """

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

        self.model: whisper.Whisper | None = None
        self.last_settings_info: dict | None = None

    def change_whisper_model(self, whisper_model_enum: WhisperModelEnum) -> None:
        """
        Change the Whisper ASR model.

        Args:
            whisper_model_enum (WhisperModelEnum): The enum value representing the Whisper model.

        Returns:
            None

        """
        self.config["audio_extractor"]["whisper_model"] = whisper_model_enum.value
        self.config_manager.save_config(self.config)
        self.logger.info(
            f"Whisper model has been changed to {whisper_model_enum.value}"
        )

    def change_whisper_device(self, whisper_device_enum: WhisperDeviceEnum) -> None:
        """
        Change the Whisper ASR device.

        Args:
            whisper_device_enum (WhisperDeviceEnum): The enum value representing the Whisper device.

        Returns:
            None

        """
        self.config["audio_extractor"]["device"] = whisper_device_enum.value
        self.config_manager.save_config(self.config)
        self.logger.info(
            f"Whisper device has been changed to {whisper_device_enum.value}"
        )

    def extract_audio(
        self, file_path: str, parent_dir: str, name: str, audio_extractor_settings: dict
    ) -> list[Sentence]:
        """
        Extract audio transcription from a file.

        Args:
            file_path (str): The path to the audio file.
            parent_dir (str): The parent directory of the audio file.
            name (str): The name of the audio file.
            audio_extractor_settings (dict): The settings for the audio extractor.

        Returns:
            list: The refined transcription as a list of dictionaries.

        """
        if self.model is None or self.is_settings_changed(audio_extractor_settings):
            try:
                self.model = whisper.load_model(
                    name=audio_extractor_settings["whisper_model"],
                    device=audio_extractor_settings["device"],
                )
            except Exception as e:
                self.logger.error(f"Failed to load model: {e}")
                return []

        audio = whisper.load_audio(file_path)
        if audio is None:
            return []

        transcription: list = self.model.transcribe(audio, fp16=False)["segments"]

        refined_transcription: list[Sentence] = self.refine_transcription(transcription)

        if not refined_transcription:
            self.logger.info("No transcription was produced.")
            return []

        self.save_transcription(parent_dir, name, refined_transcription)
        self.logger.info(f"{name} has been extracted successfully.")
        self.last_settings_info = audio_extractor_settings

        return refined_transcription

    def is_settings_changed(self, audio_extractor_settings: dict) -> bool:
        """
        Check if the audio extractor settings have changed.

        Args:
            audio_extractor_settings (dict): The current audio extractor settings.

        Returns:
            bool: True if the settings have changed, False otherwise.

        """
        return audio_extractor_settings != self.last_settings_info

    def refine_transcription(self, transcription: list) -> list[Sentence]:
        """
        Refine the transcription by rounding the start and end times.

        Args:
            transcription (list): The original transcription as a list of dictionaries.

        Returns:
            list: The refined transcription as a list of dictionaries.

        """

        refined_transcription: list[Sentence] = [
            {
                "start": round(sentence["start"], 2),
                "end": round(sentence["end"], 2),
                "text": sentence["text"],
                "translated_text": None,
            }
            for sentence in transcription
        ]

        return refined_transcription

    def save_transcription(
        self, parent_dir: str, name: str, transcription: list[Sentence]
    ) -> None:
        """
        Save the transcription to a file.

        Args:
            parent_dir (str): The parent directory of the audio file.
            name (str): The name of the audio file.
            transcription (list): The refined transcription as a list of dictionaries.

        Returns:
            None

        """
        transcription_path = f"{os.path.join(parent_dir, name)}_extracted.txt"
        if os.path.exists(transcription_path):
            self.logger.info(f"{transcription_path} already exists.")
            return

        with open(f"{os.path.join(parent_dir, name)}_extracted.txt", "w") as f:
            for sentence in transcription:
                f.write(
                    f'{sentence["start"]} ~ {sentence["end"]}\n{sentence["text"]}\n'
                )
        self.logger.info(f"{transcription_path} has been saved successfully.")

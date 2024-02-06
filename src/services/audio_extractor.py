import logging
import os

import whisper

from src.utils import config_manager
from src.utils.enums import WhisperDeviceEnum, WhisperModelEnum


class AudioExtractor:
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
        self, file_path: str, parent_dir: str, name: str, audio_extractor_settings: dict
    ) -> list:
        if self.model is None or self.is_settings_changed(
            audio_extractor_settings
        ):
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
        
        refined_transcription: list = []
        if transcription:
            refined_transcription = self.refine_transcription(transcription)
        else:
            self.logger.info("No transcription was produced.")
            return refined_transcription

        self.save_transcription(parent_dir, name, refined_transcription)
        self.logger.info(f"{name} has been extracted successfully.")
        self.last_settings_info = audio_extractor_settings

        return refined_transcription

    def is_settings_changed(self, audio_extractor_settings: dict) -> bool:
        return audio_extractor_settings != self.last_settings_info

    def refine_transcription(self, transcription: list) -> list:
        return [
            {
                "start": round(sentence["start"], 2),
                "end": round(sentence["end"], 2),
                "text": sentence["text"],
            }
            for sentence in transcription
        ]

    def save_transcription(
        self, parent_dir: str, name: str, transcription: list
    ) -> None:
        transcription_name = f"{os.path.join(parent_dir, name)}_extracted.txt"
        if os.path.exists(transcription_name):
            self.logger.info(f"{transcription_name} already exists.")
            return
        
        with open(f"{os.path.join(parent_dir, name)}_extracted.txt", "w") as file:
            for sentence in transcription:
                file.write(
                    f'{sentence["start"]} ~ {sentence["end"]}\n{sentence["text"]}\n'
                )

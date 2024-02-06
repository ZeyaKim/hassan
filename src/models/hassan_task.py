import logging
import os

from PySide6.QtGui import QStandardItemModel

from src.services import audio_extractor, subtitle_generator, translator
from src.utils.types import Sentence


class HassanTask(QStandardItemModel):
    def __init__(
        self,
        logger: logging.Logger,
        root_dir: str,
        audio_extractor: audio_extractor.AudioExtractor,
        translator: translator.Translator,
        subtitle_generator: subtitle_generator.SubtitleGenerator,
        file_path: str,
        execution_settings: dict,
    ):
        super().__init__()
        self.logger = logger
        self.root_dir = root_dir
        self.audio_extractor = audio_extractor
        self.translator = translator
        self.subtitle_generator = subtitle_generator
        self.file_path = file_path
        self.execution_settings = execution_settings

        self.parent_dir = os.path.dirname(file_path)

    def execute(self) -> None:
        base_name = os.path.basename(self.file_path)
        name, _ = os.path.splitext(base_name)

        transcription: list[Sentence] = self.audio_extractor.extract_audio(
            self.file_path,
            self.parent_dir,
            name,
            self.execution_settings["audio_extractor"],
        )
        translated_transcription: list[Sentence] = (
            self.translator.translate_transcription(
                self.parent_dir,
                name,
                self.execution_settings["translator"],
                transcription,
            )
        )
        self.subtitle_generator.generate_subtitle(
            self.file_path,
            self.parent_dir,
            name,
            self.execution_settings["subtitle_generator"],
            translated_transcription,
        )

        self.logger.info(f"Task for {name} has been executed successfully.")

import logging
import os

import pysubs2

from src.utils import config_manager
from src.utils.enums import SubtitleExtEnum
from src.utils.types import Sentence


class SubtitleGenerator:
    """Class for subtitle generator service."""

    def __init__(
        self,
        logger: logging.Logger,
        root_dir: str,
        config_manager: config_manager.ConfigManager,
        config: dict,
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

    def generate_subtitle(
        self,
        path: str,
        parent_dir: str,
        name: str,
        subtitle_settings: dict,
        translated_transcription: list[Sentence],
    ) -> None:

        subs: pysubs2.SSAFile = pysubs2.SSAFile()

        for sentence in translated_transcription:
            subs.append(self.create_ssa_event(sentence))

        subtitle_ext = subtitle_settings["subtitle_ext"]

        self.save_subtitle(parent_dir, name, subs, subtitle_ext)

        self.logger.info(f"{name} has been subtitled successfully.")

    def create_ssa_event(self, sentence: Sentence) -> pysubs2.SSAEvent:
        start_second, start_ms = map(int, str(sentence["start"]).split("."))
        end_second, end_ms = map(int, str(sentence["end"]).split("."))
        translated_text: str | None = sentence["translated_text"]

        event = pysubs2.SSAEvent(
            start=pysubs2.make_time(s=start_second, ms=start_ms),
            end=pysubs2.make_time(s=end_second, ms=end_ms),
            text=translated_text,
        )

        return event

    def save_subtitle(
        self,
        parent_dir: str,
        name: str,
        subs: pysubs2.SSAFile,
        subtitle_ext: str,
    ) -> None:
        subtitle_path = os.path.join(parent_dir, f"{name}{subtitle_ext}")

        if os.path.exists(subtitle_path):
            return

        try:
            subs.save(subtitle_path, encoding="utf-8", format_=subtitle_ext[1:])
        except Exception as e:
            self.logger.error(f"Failed to save subtitle: {e}")
            return

import concurrent.futures
import logging
import os

import deepl
import whisper
from deepl.translator import GlossaryInfo

from src.models.custom_glossary import CustomGlossary
from src.services.glossary_manager import GlossaryManager
from src.utils import config_manager
from src.utils.enums import SourceLanguageEnum, TargetLanguageEnum
from src.utils.types import Sentence


class Translator:

    def __init__(
        self,
        logger: logging.Logger,
        root_dir: str,
        config_manager: config_manager.ConfigManager,
        config: dict,
        glossary_manager: GlossaryManager,
    ):
        self.logger = logger
        self.root_dir = root_dir
        self.config_manager = config_manager
        self.config = config
        self.glossary_manager = glossary_manager

    def edit_api_key(self, api_key: str) -> bool:
        if not self._is_valid_api_key(api_key):
            self.logger.info("API key has not been changed.")
            return False

        self.config["translator"]["deepl_api_key"] = api_key
        self.config_manager.save_config(self.config)

        self.logger.info("API key has been changed successfully.")
        return True

    def _is_valid_api_key(self, api_key: str) -> bool:
        try:
            translator = deepl.Translator(api_key)
            result = translator.translate_text("test", target_lang="KO")
            if not result:
                raise Exception
        except Exception:
            self.logger.error("Invalid API key")
            return False

        self.config["translator"]["is_valid_api_key"] = True
        self.config_manager.save_config(self.config)
        return True

    def translate_transcription(
        self,
        parent_dir: str,
        name: str,
        translator_settings: dict,
        transcription: list[Sentence],
    ) -> list[Sentence]:

        api_key = translator_settings["deepl_api_key"]
        if not self._is_valid_api_key(api_key):
            return []
        translator = deepl.Translator(api_key)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(
                executor.map(
                    lambda sentence: self._translate_sentence_without_glossary(
                        sentence,
                        translator,
                        translator_settings["target_lang"],
                    ),
                    transcription,
                )
            )

        self._save_translated_transcription(parent_dir, name, results)

        self.logger.info(f"{name} has been translated successfully.")
        return results

    def _translate_sentence(
        self,
        sentence: Sentence,
        translator: deepl.Translator,
        source_lang,
        target_lang: str,
        glossary: GlossaryInfo | CustomGlossary | None,
    ) -> Sentence:
        match glossary:
            case glossary if isinstance(glossary, GlossaryInfo):
                return self._translate_sentence_with_deepl_glossary(
                    sentence, translator, source_lang, target_lang, glossary
                )
            case glossary if isinstance(glossary, CustomGlossary):
                return self._translate_sentence_with_custom_glossary(
                    sentence, translator, source_lang, target_lang, glossary
                )
            case None:
                return self._translate_sentence_without_glossary(
                    sentence, translator, source_lang, target_lang
                )

    def _translate_sentence_without_glossary(
        self,
        sentence: Sentence,
        translator: deepl.Translator,
        source_lang: str,
        target_lang: str,
    ) -> Sentence:
        translated_text = translator.translate_text(
            sentence["text"], 
            source_lang=source_lang,
            target_lang=target_lang,
        )
        if translated_text and type(translated_text) == whisper.TextResult:
            sentence["translated_text"] = translated_text.text

        return sentence

    def _translate_sentence_with_custom_glossary(
        self,
        sentence: Sentence,
        translator: deepl.Translator,
        source_lang: str,
        target_lang: str,
        glossary: CustomGlossary,
    ) -> Sentence: ...

    def _translate_sentence_with_deepl_glossary(
        self,
        sentence: Sentence,
        translator: deepl.Translator,
        source_lang: str,
        target_lang: str,
        glossary: GlossaryInfo,
    ) -> Sentence:
        translated_text = translator.translate_text(
            sentence["text"],
            source_lang=source_lang,
            target_lang=target_lang,
            glossary=glossary,
        )
        if translated_text and type(translated_text) == whisper.TextResult:
            sentence["translated_text"] = translated_text.text

        return sentence
        


    def _save_translated_transcription(
        self, parent_dir: str, name: str, transcription: list[Sentence]
    ) -> None:
        translated_transcription_path = (
            f"{os.path.join(parent_dir, name)}_translated.txt"
        )

        if os.path.exists(translated_transcription_path):
            self.logger.info(f"{translated_transcription_path} already exists.")
            return

        with open(translated_transcription_path, "w") as f:
            for sentence in transcription:
                f.write(
                    f'{sentence["start"]} ~ {sentence["end"]}\n{sentence["translated_text"]}\n'
                )
        self.logger.info(
            f"{translated_transcription_path} has been saved successfully."
        )

    def get_glossary(
        self, source_lang: SourceLanguageEnum, target_lang: TargetLanguageEnum
    ) -> dict[str, str]:
        if self.glossary_manager.is_glossary_available_language(
            source_lang, target_lang
        ):
            return self.glossary_manager.get_custom_glossary()

    def create_glossary(self) -> None:
        self.config["translator"]["glossary"] = ...
        self.config_manager.save_config(self.config)
        self.logger.info("Glossary has been saved successfully.")

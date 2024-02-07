import concurrent.futures
import os

import deepl

from src.utils.types import Sentence


class Translator:

    def __init__(self, logger, root_dir, config_manager, config):
        self.logger = logger
        self.root_dir = root_dir
        self.config_manager = config_manager
        self.config = config

    def edit_api_key(self, api_key: str) -> bool:
        if not self.is_valid_api_key(api_key):
            self.logger.info("API key has not been changed.")
            return False

        self.config["translator"]["deepl_api_key"] = api_key
        self.config_manager.save_config(self.config)

        self.logger.info("API key has been changed successfully.")
        return True

    def is_valid_api_key(self, api_key: str) -> bool:
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
        parent_dir,
        name: str,
        translator_settings: dict,
        transcription: list[Sentence],
    ) -> list[Sentence]:

        api_key = translator_settings["deepl_api_key"]
        if not self.is_valid_api_key(api_key):
            return []
        translator = deepl.Translator(api_key)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(
                executor.map(
                    lambda sentence: self.translate_sentence(
                        sentence,
                        translator,
                        translator_settings["target_lang"],
                    ),
                    transcription,
                ))

        self.save_translated_transcription(parent_dir, name, results)

        self.logger.info(f"{name} has been translated successfully.")
        return results

    def translate_sentence(self, sentence: Sentence, translator,
                           target_lang) -> Sentence:
        translated_text = translator.translate_text(sentence["text"],
                                                    target_lang=target_lang)
        if translated_text:
            sentence["translated_text"] = translated_text.text

        return sentence

    def save_translated_transcription(self, parent_dir: str, name: str,
                                      transcription: list[Sentence]) -> None:
        translated_transcription_path = (
            f"{os.path.join(parent_dir, name)}_translated.txt")

        if os.path.exists(translated_transcription_path):
            self.logger.info(
                f"{translated_transcription_path} already exists.")
            return

        with open(translated_transcription_path, "w") as f:
            for sentence in transcription:
                f.write(
                    f'{sentence["start"]} ~ {sentence["end"]}\n{sentence["translated_text"]}\n'
                )
        self.logger.info(
            f"{translated_transcription_path} has been saved successfully.")

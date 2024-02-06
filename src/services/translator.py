import os

import concurrent.futures

import deepl


class Translator:
    def __init__(self, logger, root_dir, config_manager, config):
        self.logger = logger
        self.root_dir = root_dir
        self.config_manager = config_manager
        self.config = config

    # TODO: api 키를 변경하는 로직을 구현해야 합니다.
    def change_api_key(self, api_key: str) -> None:
        if not self.is_valid_api_key(api_key):
            self.logger.error("Invalid API key")
            return

    # TODO: api 키를 검증하는 로직을 구현해야 합니다.
    def is_valid_api_key(self, api_key: str) -> bool:
        return True

    def translate_transcription(
        self,
        parent_dir,
        name: str,
        translator_settings: dict,
        transcription: list,
    ) -> list:

        api_key = translator_settings["translator"]["api_key"]
        if not self.is_valid_api_key(api_key):
            return []

        translator = deepl.Translator(api_key)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(
                executor.map(
                    lambda sentence: self.translate_sentence(sentence, translator, translator_settings["translator"]["target_lang"]),
                    transcription,
                )
            )

        self.save_translated_transcription(parent_dir, name, results)

        self.logger.info(f"{name} has been translated successfully.")
        return results

    def translate_sentence(self, translator, sentence, target_lang) -> dict:
        translated_text = translator.translate_text(sentence["text"], target_lang=target_lang)
        if translated_text:
            sentence["translated_text"] = translated_text
        
        return sentence

    def save_translated_transcription(
        self, parent_dir: str, name: str, transcription: list
    ) -> None:
        translated_transcription_name = f"{os.path.join(parent_dir, name)}_translated.json"
import logging

import deepl
import toml


class Translator:
    def __init__(self):
        ...

    def load_api_key(self):
        with open("keys.toml", "r") as f:
            config = toml.load(f)
            api_key = config["api_key"]["deepl"]
        return api_key

    def is_valid_api_key(self, api_key):
        try:
            translator = deepl.Translator(api_key)
            original_text = "바퀴"
            translator.translate_text(original_text, target_lang="EN-US")
            return True
        except Exception as exc:
            logging.error(exc)

        logging.info("Invalid API key")
        return False

    def edit_api_key(self, new_api_key):
        if self.is_valid_api_key(new_api_key):
            config = toml.load("keys.toml")
            config["api_key"]["deepl"] = new_api_key
            with open("keys.toml", "w") as f:
                toml.dump(config, f)
                logging.info(f"API key is edited, new API key is {new_api_key}")
        else:
            logging.info("Failed to edit API key")

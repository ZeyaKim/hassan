import logging
import os

import deepl
import toml


class Translator:
    def __init__(self):
        self.translator = None

    def load_api_key(self):
        logging.info("Loading DeepL API key")
        with open("keys.toml", "r") as f:
            config = toml.load(f)
            api_key = config["api_key"]["deepl"]
        logging.info("API key loaded successfully")
        return api_key

    def is_valid_api_key(self, api_key):
        logging.info("Validating API key")
        try:
            translator = deepl.Translator(api_key)
            original_text = "바퀴"
            translator.translate_text(original_text, target_lang="EN-US")
            logging.info("API key is valid")
            return True
        except Exception as exc:
            logging.error(f"Invalid API key: {exc}")
            return False

    def edit_api_key(self, new_api_key):
        logging.info("Editing API key")
        if self.is_valid_api_key(new_api_key):
            config = toml.load("keys.toml")
            config["api_key"]["deepl"] = new_api_key
            self.translator = deepl.Translator(new_api_key)
            with open("keys.toml", "w") as f:
                toml.dump(config, f)
                logging.info(f"API key updated successfully to {new_api_key}")
        else:
            logging.error("Failed to update API key")

    def translate(self, file_path, transcription):
        logging.info(f"Starting translation for {file_path}")

        util_logger = logging.getLogger("util")
        util_logger.setLevel(logging.DEBUG)

        if self.is_valid_api_key(self.load_api_key()) and self.translator is None:
            self.translator = deepl.Translator(self.load_api_key())
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        parent_folder_path = os.path.dirname(file_path)

        translated_transcription = []
        try:
            with open(
                os.path.join(parent_folder_path, f"{file_name}_translated.txt"), "w"
            ) as f:
                for sentence in transcription:
                    try:
                        translated_text = str(
                            self.translator.translate_text(
                                sentence["text"], target_lang="KO"
                            )
                        )

                        translated_transcription.append(
                            {
                                "start": sentence["start"],
                                "end": sentence["end"],
                                "translated_text": translated_text,
                            }
                        )
                        f.write(
                            f"{sentence['start']} ~ {sentence['end']}\n{translated_text}\n"
                        )
                    except Exception as exc:
                        logging.error(
                            f"Failed to translate text: {sentence['text']}: {exc}"
                        )
        except Exception as exc:
            error_msg = (
                f"Failed to create translated transcription file for {file_path}: {exc}"
            )
            logging.error(error_msg)

        return translated_transcription

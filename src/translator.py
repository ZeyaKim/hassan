import logging
import os

import deepl
import toml


class Translator:
    def __init__(self):
        if self.is_valid_api_key(self.load_api_key()):
            self.translator = deepl.Translator(self.load_api_key())

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
            self.translator = deepl.Translator(new_api_key)
            with open("keys.toml", "w") as f:
                toml.dump(config, f)
                logging.info(f"API key is edited, new API key is {new_api_key}")
        else:
            logging.info("Failed to edit API key")

    def translate(self, transcription, file_path):
        file_name = os.path.basename(file_path).split(".")[0]
        parent_folder_path = os.path.dirname(file_path)

        translated_transcription = []
        try:
            with open(
                os.path.join(parent_folder_path, f"{file_name}_translated.txt"), "w"
            ) as f:
                for sentence in transcription:
                    try:
                        translated_text = str(
                            self.translate_text(sentence["text"], target_lang="KO")
                        )
                        
                        translated_transcription.append({
                            'start': sentence['start'],
                            'end': sentence['end'],
                            'translated_text': translated_text
                        })
                        f.write(
                            f"{sentence['start']} ~ {sentence['end']}\n{translated_text}\n\n"
                        )
                    except Exception as exc:
                        error_msg = f"Failed to translate text {sentence['text']}: {exc}"
                        logging.error(error_msg)
        except Exception as exc:
            error_msg = f"Failed to making translated transcription file from {file_path}: {exc}"
            logging.error(error_msg)
        
        return translated_transcription
        
        

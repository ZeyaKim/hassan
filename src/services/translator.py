import logging
import os
import pathlib
import dotenv
import deepl
import concurrent.futures
from PyQt5.QtCore import pyqtSignal, QObject


class Translator(QObject):
    api_key_changed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.logger = logging.getLogger(__name__)
        deepl_logger = logging.getLogger("deepl")
        deepl_logger.setLevel(logging.CRITICAL + 1)

        self.root_dir = pathlib.Path(os.environ["ROOT_DIR"])
        self.env_path = self.root_dir / ".env"

        self.setting = {}
        self.deepl_api_key = self.load_deepl_api_key()
        self.translator = None

    def load_deepl_api_key(self):
        if not self.env_path.exists():
            with self.env_path.open("w") as f:
                f.write('DEEPL_API_KEY=""')
            return ""
        else:
            dotenv.load_dotenv(self.env_path)
            deepl_api_key = os.getenv("DEEPL_API_KEY")
            return deepl_api_key

    def validate_api_key(self, api_key):
        try:
            self.translator = deepl.Translator(auth_key=api_key)
            self.logger.info("API key is valid")
            return True
        except Exception as e:
            self.logger.error(f"Failed to validate API key: {e}")
            return False

    def set_api_key(self, api_key):
        if self.validate_api_key(api_key):
            self.deepl_api_key = api_key
            dotenv.set_key(self.env_path, "DEEPL_API_KEY", api_key)
            self.logger.info(f"Now, API key is set to {api_key}")
            self.api_key_changed.emit()
        else:
            self.logger.error("Failed to set API key")

    def translate(self, transcription, file_path):
        if self.translator is None:
            self.translator = deepl.Translator(auth_key=self.deepl_api_key)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            translated_transcription = list(
                executor.map(
                    lambda sentence: {
                        "start": sentence["start"],
                        "end": sentence["end"],
                        "translated_text": self.translate_sentence(sentence["text"]),
                    },
                    transcription,
                )
            )

        self.save_translated_text(translated_transcription, file_path)

        # 번역된 문장들의 리스트 반환
        return translated_transcription

    def translate_sentence(self, text):
        result = str(
            self.translator.translate_text(text, source_lang="JA", target_lang="KO")
        )
        return result

    def save_translated_text(self, translated_transcription, file_path):
        translated_trancription_path = (
            file_path.parent / f"{file_path.stem}_translated.txt"
        )
        with translated_trancription_path.open("w", encoding="utf-8") as f:
            for sentence in translated_transcription:
                line = f"{sentence['start']} - {sentence['end']}\n{sentence['translated_text']}\n\n"
                f.write(line)

    def get_masked_api_key(self):
        if self.deepl_api_key == "":
            return ""
        else:
            return f"{self.deepl_api_key[:4]}{'*' * 16}{self.deepl_api_key[-4:]}"

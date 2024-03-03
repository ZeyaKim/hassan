import logging
import os
import pathlib
import dotenv
import deepl


class Translator:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
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

    def validate_api_kdy(self, api_key):
        try:
            self.translator = deepl.Translator(auth_key=api_key)
            self.logger.info("API key is valid")
            return True
        except Exception as e:
            self.logger.error(f"Failed to validate API key: {e}")
            return False

    def set_api_key(self, api_key):
        if self.validate_api_kdy(api_key):
            self.deepl_api_key = api_key
            dotenv.set_key(self.env_path, "DEEPL_API_KEY", api_key)
            self.logger.info(f"Now, API key is set to {api_key}")
        self.logger.warning("API key is not set")

    def translate(self, transcription, file_path):
        if self.translator is None:
            self.translator = deepl.Translator(auth_key=self.deepl_api_key)

    def translate_sentence(self, sentence): ...

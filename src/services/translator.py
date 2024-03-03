import logging
import os
import pathlib


class Translator:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.root_dir = pathlib.Path(os.environ["ROOT_DIR"])
        self.env_path = self.root_dir / ".env"

        self.setting = {}
        self.deepl_api_key = self.load_deepl_api_key()

    def load_deepl_api_key(self):
        if self.env_path.exists():
            with self.env_path.open("w") as f:
                f.write('DEEPL_API_KEY=""')

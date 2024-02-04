import logging
import os

import toml


class ConfigManager:
    def __init__(self, logger: logging.Logger, root_dir: str):
        self.logger = logger
        self.config_path = os.path.join(root_dir, "config.toml")

    def load_config(self) -> dict:
        try:
            with open(self.config_path, "r") as f:
                return toml.load(f)
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
        return {}

    def save_config(self, config: dict) -> None:
        try:
            with open(self.config_path, "w") as f:
                toml.dump(config, f)
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")

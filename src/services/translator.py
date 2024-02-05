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
        file_path,
        parent_dir,
        name: str,
        execution_settings: dict,
        description: list,
    ) -> dict:

        # TODO: Implement translation

        translated_description: dict = {}

        self.logger.info(f"{name} has been translated successfully.")

        return translated_description

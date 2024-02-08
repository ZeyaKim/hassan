import os

import deepl
import toml

from src.utils.enums import (
    GlossaryAvailableLanguageEnum,
    SourceLanguageEnum,
    TargetLanguageEnum,
)
from src.utils.types import GlossaryPair


class GlossaryManager:
    def __init__(self, root_dir: str):
        self.glossary_dir_path = os.path.join(root_dir, "glossary")
        if not os.path.exists(self.glossary_dir_path):
            os.makedirs(self.glossary_dir_path)

    def is_glossary_available_language(
        self, source_lang: SourceLanguageEnum, target_lang: TargetLanguageEnum
    ) -> bool:
        return (
            source_lang.value in GlossaryAvailableLanguageEnum
            and target_lang.value in GlossaryAvailableLanguageEnum
        )

    def get_glossary_entries(
        self, source_lang: SourceLanguageEnum, target_lang: TargetLanguageEnum
    ) -> dict[str, str]:
        glossary_path = os.path.join(
            self.glossary_dir_path, self._glossary_file_name(source_lang, target_lang)
        )

        if not os.path.exists(glossary_path):
            self._create_glossary(source_lang, target_lang)
        return self._load_glossary(source_lang, target_lang)

    def _glossary_file_name(
        self, source_lang: SourceLanguageEnum, target_lang: TargetLanguageEnum
    ) -> str:
        return f"from_{source_lang}_to_{target_lang}.txt"

    def _create_glossary_file(
        self, source_lang: SourceLanguageEnum, target_lang: TargetLanguageEnum
    ) -> None:
        glossary: dict[str, str] = {}
        self.save_glossary(source_lang, target_lang, glossary)

    def _load_glossary(
        self, source_lang: SourceLanguageEnum, target_lang: TargetLanguageEnum
    ) -> GlossaryPair:
        with open(
            os.path.join(
                self.glossary_dir_path,
                self._glossary_file_name(source_lang, target_lang),
            ),
            "r",
        ) as f:
            glossary = toml.load(f)

        return glossary

    def add_pair_to_glossary(
        self, source_lang: SourceLanguageEnum, target_lang: TargetLanguageEnum, glossary
    ) -> None: ...

    def delete_glossary_pair_from_glossary(
        self, source_lang: SourceLanguageEnum, target_lang: TargetLanguageEnum, glossary
    ) -> None: ...

    def _save_glossary(
        self,
        source_lang: SourceLanguageEnum,
        target_lang: TargetLanguageEnum,
        glossary: deepl.G,
    ) -> None:
        glossary_file_name = self._glossary_file_name(source_lang, target_lang)

        with open(os.path.join(self.glossary_dir_path, glossary_file_name), "w") as f:
            toml.dump(glossary, f)

"""
이 모듈은 DeepL 번역 API를 활용하여 텍스트 번역 기능을 제공하는 Translator 클래스를 정의합니다. 
주요 기능으로는 DeepL API 키의 로드 및 유효성 검증, 번역기 인스턴스의 초기화, 텍스트의 병렬 번역 처리가 포함됩니다.
본 모듈은 효율적인 번역 작업을 위해 concurrent.futures를 사용하여 멀티스레딩을 구현합니다.

Classes:
    Sentence: 번역할 문장의 정보를 담는 타입 지정 사전.
    Translator: DeepL API를 활용하여 텍스트를 번역하는 기능을 제공하는 클래스.
"""
import concurrent.futures
import logging
import os
from typing import Any, TypedDict

import deepl
import toml
from deepl.api_data import TextResult


class Sentence(TypedDict):
    """
    DeepL 번역 API를 사용하는 번역 과정에서 필요한 문장의 정보를 담는 타입 지정 사전.

    Attributes:
        start (float): 문장의 시작 시간.
        end (float): 문장의 종료 시간.
        text (str): 번역할 문장의 텍스트.
    """
    start: float
    end: float
    text: str


class Translator:
    """
    DeepL API를 사용하여 텍스트 번역을 수행하는 클래스.

    이 클래스는 DeepL API 키를 로드하고, 번역 모델을 관리하며, 주어진 텍스트에 대한 번역을 수행합니다.
    병렬 처리를 사용하여 여러 문장의 번역을 효율적으로 처리할 수 있습니다.

    Attributes:
        translator (deepl.Translator | None): DeepL 번역기 인스턴스.
        api_key (str | None): DeepL API 키.
    """

    def __init__(self):
        self.translator: deepl.Translator | None = None
        self.api_key: str | None = None

    def load_api_key(self) -> str:
        """
        `keys.toml` 파일에서 DeepL API 키를 로드합니다.

        Returns:
            str: 로드된 DeepL API 키.
        """
        logging.info("Loading DeepL API key")
        with open("keys.toml", "r") as f:
            config: dict[str, Any] = toml.load(f)
            api_key: str = config["api_key"]["deepl"]
        logging.info("API key loaded successfully")
        return api_key

    def is_valid_api_key(self, api_key: str) -> bool:
        """
        제공된 DeepL API 키의 유효성을 검증합니다.

        Args:
            api_key (str): 검증할 DeepL API 키.

        Returns:
            bool: API 키가 유효한 경우 True, 그렇지 않으면 False.
        """
        logging.info("Validating API key")
        try:
            translator: deepl.Translator = deepl.Translator(api_key)
            original_text: str = "바퀴"
            translator.translate_text(original_text, target_lang="EN-US")
            logging.info("API key is valid")
            return True
        except Exception as exc:
            logging.error(f"Invalid API key: {exc}")
            return False

    def edit_api_key(self, new_api_key: str) -> None:
        """
        `keys.toml` 파일에 새로운 DeepL API 키를 저장합니다.

        Args:
            new_api_key (str): 저장할 새 DeepL API 키.
        """
        logging.info("Editing API key")
        if self.is_valid_api_key(new_api_key):
            config: dict[str, Any] = toml.load("keys.toml")
            config["api_key"]["deepl"]: str = new_api_key
            self.api_key: str = new_api_key
            with open("keys.toml", "w") as f:
                toml.dump(config, f)
                logging.info(f"API key updated successfully to {new_api_key}")
        else:
            logging.error("Failed to update API key")

    def translate_concurrent(self, sentence: Sentence) -> Sentence:
        """
        주어진 문장을 병렬로 번역합니다.

        Args:
            sentence (Sentence): 번역할 문장 정보를 담은 사전.

        Returns:
            Sentence: 번역된 문장 정보를 담은 사전.
        """
        translated_text: TextResult | list[TextResult] = self.translator.translate_text(
            sentence["text"], target_lang="KO"
        )
        sentence["text"]: str = translated_text.text
        return sentence

    def translate(self, file_path: str, transcription: list[Sentence]) -> list[Sentence]:
        """
        오디오 파일에서 추출된 문장을 번역합니다.

        Args:
            file_path (str): 오디오 파일의 경로.
            transcription (list[Sentence]): 번역할 문장 정보가 담긴 리스트.

        Returns:
            list[Sentence]: 번역된 문장 정보를 담은 리스트.
        """
        logging.info(f"Starting translation for {file_path}")

        if self.api_key is None:
            self.api_key: str = self.load_api_key()
        if self.is_valid_api_key(self.api_key) and self.translator is None:
            self.translator: deepl.Translator = deepl.Translator(self.api_key)

        file_name: str = os.path.splitext(os.path.basename(file_path))[0]
        parent_folder_path: str = os.path.dirname(file_path)

        translated_transcription: list[Sentence] = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            translated_transcription: list[Sentence] = list(
                executor.map(
                    lambda sentence: self.translate_concurrent(sentence), transcription
                )
            )

        try:
            with open(
                os.path.join(parent_folder_path, f"{file_name}_translated.txt"), "w"
            ) as f:
                for sentence in translated_transcription:
                    try:
                        f.write(
                            f"{sentence['start']} ~ {sentence['end']}\n{sentence['text']}\n"
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

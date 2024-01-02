"""
이 모듈은 Whisper API를 사용하여 오디오 파일에서 텍스트를 추출하는 기능을 제공합니다.
주요 기능으로는 Whisper 모델의 로드 및 설정 변경, 오디오 파일에서의 텍스트 추출 및 저장이 포함됩니다.

Classes:
    Sentence: 추출된 텍스트의 문장 정보를 담는 타입 지정 사전.
    AudioExtractor: 오디오 파일에서 텍스트를 추출하고 저장하는 클래스.
"""

import logging
import os
from typing import Any, TypedDict

import toml
import whisper


class Sentence(TypedDict):
    """
    오디오에서 추출된 텍스트의 문장 정보를 정의하는 타입 지정 사전.

    Attributes:
        start (float): 문장의 시작 시간.
        end (float): 문장의 종료 시간.
        text (str): 추출된 문장의 텍스트.
    """
    start: float
    end: float
    text: str


class AudioExtractor:
    """
    Whisper API를 사용하여 오디오 파일에서 텍스트를 추출하는 클래스입니다.

    Whisper 모델을 로드하고, 오디오 파일을 처리하여 텍스트 추출을 수행한 뒤, 결과를 저장합니다.

    Attributes:
        models (list[str]): 사용 가능한 Whisper 모델 목록.
        current_model (str): 현재 로드된 Whisper 모델.
        last_model (str): 마지막으로 사용된 Whisper 모델.
        model (whisper.Whisper | None): Whisper 모델 인스턴스.
    """

    def __init__(self):
        """
        AudioExtractor 클래스의 인스턴스를 초기화합니다.
        """
        self.models: list[str] = ["small", "medium", "large"]
        self.current_model: str = self.load_model_config()
        self.last_model: str = self.current_model
        self.model: whisper.Whisper | None = None

    def load_model_config(self) -> str:
        """
        `config.toml` 파일에서 Whisper 모델 설정을 로드합니다.

        Returns:
            str: 로드된 Whisper 모델 이름.
        """
        logging.info("Loading model configuration")
        with open("config.toml", "r") as f:
            config: dict[str, Any] = toml.load(f)
            model: str = config["whisper"]["model"]
        return model

    def change_model_config(self, model: str) -> None:
        """
        `config.toml` 파일에 새로운 Whisper 모델 설정을 저장합니다.

        Args:
            model (str): 저장할 새 Whisper 모델 이름.
        """
        logging.info(f"Changing model configuration to {model}")
        with open("config.toml", "r") as f:
            config = toml.load(f)
        config["whisper"]["model"] = model
        with open("config.toml", "w") as f:
            toml.dump(config, f)
            self.current_model: str = model
            logging.info(f"Model configuration updated to {model}")

    def load_model(self) -> None:
        """
        현재 설정된 Whisper 모델을 로드합니다. 모델이 변경되었거나 아직 로드되지 않았을 경우에만 로드를 수행합니다.
        """
        if self.current_model != self.last_model or self.model is None:
            try:
                logging.info(f"Loading Whisper model: {self.current_model}")
                self.model = whisper.load_model(self.current_model, device="cuda")
                self.last_model = self.current_model
            except Exception as exc:
                logging.error(f"Failed to load Whisper model: {exc}")
                self.model = None

    def save_transcription(self, transcription: list[Sentence], file_path: str) -> None:
        """
        추출된 텍스트를 파일로 저장합니다.

        Args:
            transcription (list[Sentence]): 추출된 문장 정보를 포함하는 리스트.
            file_path (str): 저장할 파일의 경로.
        """
        try:
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            parent_folder_path = os.path.dirname(file_path)
            transcription_file_path = os.path.join(
                parent_folder_path, f"{file_name}_transcription.txt"
            )
            logging.info(f"Writing transcription to {transcription_file_path}")
            with open(transcription_file_path, "w") as f:
                for sentence in transcription:
                    f.write(
                        f'{sentence["start"]} ~ {sentence["end"]}\n{sentence["text"]}\n'
                    )
            logging.info("Transcription successfully saved")
        except Exception as exc:
            logging.error(f"Failed to save transcription file for {file_path}: {exc}")

    def extract_transcription(self, file_path: str) -> list[Sentence]:
        """
        주어진 파일 경로의 오디오에서 텍스트를 추출합니다.

        Args:
            file_path (str): 오디오 파일의 경로.

        Returns:
            list[Sentence]: 추출된 문장 정보를 포함하는 리스트.
        """
        logging.info(f"Starting transcription for {file_path}")
        self.load_model()

        try:
            logging.info(f"Loading audio file: {file_path}")
            audio = whisper.load_audio(file_path)
        except Exception as exc:
            error_msg = f"Failed to load audio from {file_path}: {exc}"
            logging.error(error_msg)
            return []

        try:
            logging.info("Transcribing audio")
            transcription = self.model.transcribe(audio, fp16=False)
        except Exception as exc:
            error_msg = f"Failed to transcribe audio from {file_path}: {exc}"
            logging.error(error_msg)
            return []

        segment = transcription["segments"]

        transcription_dict = [
            {
                "start": round(sentence["start"], 2),
                "end": round(sentence["end"], 2),
                "text": sentence["text"],
            }
            for sentence in segment
        ]

        self.save_transcription(transcription_dict, file_path)
        return transcription_dict

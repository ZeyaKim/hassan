"""
이 모듈은 번역된 텍스트를 기반으로 자막 파일을 생성하는 기능을 제공합니다.
pysubs2 라이브러리를 사용하여 ASS 및 SRT 형식의 자막을 처리하며, 사용자가 지정한 확장자 설정을 로드하고 수정할 수 있는 기능을 포함하고 있습니다.
번역된 자막 데이터를 효과적으로 시각적 자막 형식으로 변환하는 데 사용됩니다.

Classes:
    Sentence: 자막 이벤트 생성에 필요한 문장의 시작 시간, 종료 시간, 번역된 텍스트 정보를 포함합니다.
    SubtitleGenerator: 번역된 텍스트를 사용하여 자막 이벤트를 생성하고, 이를 ASS 또는 SRT 형식의 자막 파일로 저장합니다.
"""

import logging
import os
from typing import Any, Dict, List, TypedDict

import pysubs2
import toml


class Sentence(TypedDict):
    """
    자막 이벤트를 생성하기 위한 문장 정보를 정의하는 타입입니다.

    Attributes:
        start (float): 문장의 시작 시간.
        end (float): 문장의 종료 시간.
        text (str): 문장의 텍스트.
    """
    start: float
    end: float
    text: str


class SubtitleGenerator:
    """
    번역된 텍스트를 사용하여 자막 파일을 생성하는 클래스입니다.

    pysubs2 라이브러리를 사용하여 ASS 또는 SRT 형식의 자막 이벤트를 생성하고 저장합니다. 
    사용자가 지정한 확장자 설정을 로드하고 수정할 수 있으며, 번역된 텍스트를 시각적 자막 형식으로 변환하는 기능을 제공합니다.

    Attributes:
        subs_exts (List[str]): 지원하는 자막 파일 확장자 목록.
        ext (str): 현재 설정된 자막 파일 확장자.
    """

    def __init__(self):
        """
        SubtitleGenerator 클래스의 인스턴스를 초기화합니다.
        """
        self.subs_exts: List[str] = ["srt", "ass"]
        self.ext = self.load_subtitle_ext()

    def create_event(self, sentence: Sentence) -> pysubs2.SSAEvent:
        """
        주어진 문장 정보를 바탕으로 pysubs2.SSAEvent 객체를 생성합니다.

        Args:
            sentence (Sentence): 자막 이벤트 정보를 담고 있는 사전. 'start', 'end', 'text' 키를 포함해야 합니다.

        Returns:
            pysubs2.SSAEvent: 생성된 자막 이벤트 객체.
        """
        start_second, start_ms = map(int, str(sentence["start"]).split("."))
        end_second, end_ms = map(int, str(sentence["end"]).split("."))
        text: str = sentence["text"]

        event = pysubs2.SSAEvent(
            start=pysubs2.make_time(s=start_second, ms=start_ms),
            end=pysubs2.make_time(s=end_second, ms=end_ms),
            text=text,
        )

        return event

    def load_subtitle_ext(self):
        """
        `config.toml` 파일에서 현재 설정된 자막 확장자를 로드합니다.

        Returns:
            str: 현재 설정된 자막 파일 확장자.
        """
        with open("config.toml", "r") as f:
            config: Dict[str, Any] = toml.load(f)
            subtitle_ext: str = config["pysubs2"]["subtitle_ext"]
        return subtitle_ext

    def edit_subtitle_ext(self, subtitle_ext: str):
        """
        자막 파일의 확장자를 변경합니다. 변경 사항은 `config.toml` 파일에 저장됩니다.

        Args:
            subtitle_ext (str): 새로 설정할 자막 파일 확장자.
        """
        if subtitle_ext in self.subs_exts:
            with open("config.toml", "r") as f:
                config: Dict[str, Any] = toml.load(f)
            config["pysubs2"]["subtitle_ext"] = subtitle_ext
            with open("config.toml", "w") as f:
                toml.dump(config, f)
                self.ext = subtitle_ext

    def generate_subtitle(
        self, file_path: str, translated_transcription: List[Sentence]
    ):
        """
        번역된 텍스트를 바탕으로 자막 파일을 생성합니다.

        Args:
            file_path (str): 원본 비디오 파일의 경로.
            translated_transcription (List[Sentence]): 번역된 문장을 포함하는 리스트.

        자막 파일은 원본 파일 이름에 현재 설정된 확장자를 추가하여 같은 위치에 저장됩니다.
        """
        logging.info(f"Starting subtitle generation for {file_path}")
        file_name: str = os.path.splitext(os.path.basename(file_path))[0]
        parent_folder_path: str = os.path.dirname(file_path)

        subs: pysubs2.SSAFile = pysubs2.SSAFile()

        try:
            for sentence in translated_transcription:
                subs.append(self.create_event(sentence))

            subs_path: str = os.path.join(parent_folder_path, f"{file_name}.{self.ext}")
            subs.save(
                subs_path,
                encoding="utf-8",
            )
            logging.info(f"Subtitle successfully generated at {subs_path}")

        except Exception as exc:
            logging.error(f"Error while generating subtitle for {file_path}: {exc}")

        logging.info(f"Subtitle is generated at {parent_folder_path}")

"""
Subtitle Generator Module.

이 모듈은 번역된 텍스트를 바탕으로 자막 파일을 생성하는 기능을 제공합니다. 
주로 pysubs2 라이브러리를 사용하여 ASS와 SRT 형식의 자막을 처리하며, 
사용자가 지정한 확장자 설정을 로드하고 수정할 수 있는 기능도 포함합니다.

주요 클래스:
- SubtitleGenerator: 번역된 텍스트를 사용하여 자막 이벤트를 생성하고, 
  이를 ASS 또는 SRT 형식의 자막 파일로 저장합니다.
"""
import logging
import os
from typing import Any, Dict, List, TypedDict

import pysubs2
import toml


class Sentence(TypedDict):
    start: float
    end: float
    text: str


class SubtitleGenerator:
    """
    pysubs2 라이브러리를 이용해 자막을 제작하는 클래스.
    """

    def __init__(self):
        self.subs_exts: List[str] = ["srt", "ass"]
        self.ext = self.load_subtitle_ext()

    def create_event(self, sentence: Sentence) -> pysubs2.SSAEvent:
        """
        시작과 끝 시간, 문장으로 이루어진 Dictionary를 받아 pySubs2.SSAEvent를 생성하고 반환합니다.
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
        config.toml 설정 파일을 조회해서 현재 설정된 자막 확장자를 불러옵니다.
        """
        with open("config.toml", "r") as f:
            config: Dict[str, Any] = toml.load(f)
            subtitle_ext: str = config["pysubs2"]["subtitle_ext"]
        return subtitle_ext

    def edit_subtitle_ext(self, subtitle_ext: str):
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

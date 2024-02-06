from typing import TypedDict


class Sentence(TypedDict):
    start: float
    end: float
    text: str | None
    translated_text: str | None
from typing import TypedDict, Iterable


class Sentence(TypedDict):
    start: float
    end: float
    text: str | Iterable[str]
    translated_text: str | None

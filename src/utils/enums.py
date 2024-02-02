from enum import Enum


class SubtitleExtEnum(Enum):
    SRT = "srt"
    ASS = "ass"

class ExtractableExtEnum(Enum):
    MP3 = "mp3"
    WAV = "wav"

class WhisperModelEnum(Enum):
    SMALL = "small"
    Medium = "medium"
    Large = "large"

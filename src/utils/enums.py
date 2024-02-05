from enum import Enum


class SubtitleExtEnum(Enum):
    """Enum class for subtitle file extensions."""

    SRT = ".srt"
    ASS = ".ass"


class ExtractableExtEnum(Enum):
    """Enum class for extractable file extensions."""

    MP3 = ".mp3"
    WAV = ".wav"


class WhisperModelEnum(Enum):
    """Enum class for whisper model sizes."""

    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

class WhisperDeviceEnum(Enum):
    """Enum class for whisper devices """
    
    CPU = "cpu"
    CUDA = "cuda"
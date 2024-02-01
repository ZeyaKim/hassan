from enum import Enum

class SubtitleExtEnum(Enum):
    SRT = "srt"
    ASS = "ass"
    
    
class WhisperModelEnum(Enum):
    SMALL = "small"
    Medium = "medium"
    Large = "large"
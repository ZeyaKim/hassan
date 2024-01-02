from enum import Enum

class SubtitleExtEnum(Enum):
    SRT = 'srt'
    ASS = 'ass'
    
class WhisperModelEnum(Enum):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
    
class AvailableAudioExtEnum(Enum):
    MP3 = 'mp3'
    WAV = 'wav'
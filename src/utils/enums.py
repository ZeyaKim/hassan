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
    """Enum class for whisper devices"""

    CPU = "cpu"
    CUDA = "cuda"


class SourceLanguageEnum(Enum):
    ARABIC = "AR"
    BULGARIAN = "BG"
    CZECH = "CS"
    DANISH = "DA"
    GERMAN = "DE"
    GREEK = "EL"
    ENGLISH = "EN"
    SPANISH = "ES"
    ESTONIAN = "ET"
    FINNISH = "FI"
    FRENCH = "FR"
    HUNGARIAN = "HU"
    INDONESIAN = "ID"
    ITALIAN = "IT"
    JAPANESE = "JA"
    KOREAN = "KO"
    LITHUANIAN = "LT"
    LATVIAN = "LV"
    NORWEGIAN = "NB"
    DUTCH = "NL"
    POLISH = "PL"
    PORTUGUESE = "PT"
    ROMANIAN = "RO"
    RUSSIAN = "RU"
    SLOVAK = "SK"
    SLOVENIAN = "SL"
    SWEDISH = "SV"
    TURKISH = "TR"
    UKRAINIAN = "UK"
    CHINESE = "ZH"


class TargetLanguageEnum(Enum):
    ARABIC = "AR"
    BULGARIAN = "BG"
    CZECH = "CS"
    DANISH = "DA"
    GERMAN = "DE"
    GREEK = "EL"
    ENGLISH_GB = "EN-GB"  # 영어 (영국)
    ENGLISH_US = "EN-US"  # 영어 (미국)
    SPANISH = "ES"
    ESTONIAN = "ET"
    FINNISH = "FI"
    FRENCH = "FR"
    HUNGARIAN = "HU"
    INDONESIAN = "ID"
    ITALIAN = "IT"
    JAPANESE = "JA"
    KOREAN = "KO"
    LITHUANIAN = "LT"
    LATVIAN = "LV"
    NORWEGIAN = "NB"  # 노르웨이어 (Bokmål)
    DUTCH = "NL"
    POLISH = "PL"
    PORTUGUESE_BR = "PT-BR"  # 포르투갈어 (브라질)
    PORTUGUESE_PT = "PT-PT"  # 포르투갈어 (유럽)
    ROMANIAN = "RO"
    RUSSIAN = "RU"
    SLOVAK = "SK"
    SLOVENIAN = "SL"
    SWEDISH = "SV"
    TURKISH = "TR"
    UKRAINIAN = "UK"
    CHINESE_SIMPLIFIED = "ZH"  # 중국어 (간체)


class GlossaryAvailableLanguageEnum(Enum):
    JAPANESE = "JA"
    PORTUGUESE = "PT"
    FRANCE = "FR"
    GERMAN = "DE"
    ITALIAN = "IT"
    ENGLISH = "EN"
    CHINESE_SIMPLIFIED = "ZH"
    POLISH = "PL"

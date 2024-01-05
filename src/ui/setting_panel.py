from PySide6.QtWidgets import QVBoxLayout
from src.audio_extractor import AudioExtractor
from src.translator import Translator
from src.subtitle_generator import SubtitleGenerator


class SettingPanel(QVBoxLayout):
    def __init__(self,
                 audio_extractor: AudioExtractor,
                 translator: Translator,
                 subtitle_generator: SubtitleGenerator) -> None:
        super().__init__()
        self.initUI()

import logging

from PySide6.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout, QWidget


class SettingsPanel(QWidget):
    def __init__(self, logger: logging.Logger, root_dir: str):
        super().__init__()

        self.logger = logger
        self.root_dir = root_dir

        self.logger.debug("Initializing settings panel")

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        group_box = QGroupBox("Settings")
        group_box_layout = QVBoxLayout()
        group_box.setLayout(group_box_layout)

        translator_group_box = QGroupBox("Translator")
        translator_layout = QVBoxLayout()
        translator_group_box.setLayout(translator_layout)

        group_box_layout.addWidget(translator_group_box)

        h_layout = QHBoxLayout()

        audio_extractor_group_box = QGroupBox("Audio Extractor")
        audio_extractor_layout = QVBoxLayout()
        audio_extractor_group_box.setLayout(audio_extractor_layout)

        h_layout.addWidget(audio_extractor_group_box)

        subtitle_generator_group_box = QGroupBox("Subtitle Generator")
        subtitle_generator_layout = QVBoxLayout()
        subtitle_generator_group_box.setLayout(subtitle_generator_layout)

        h_layout.addWidget(subtitle_generator_group_box)

        group_box_layout.addLayout(h_layout)

        layout.addWidget(group_box)

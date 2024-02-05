import logging

from dependency_injector import providers
from PySide6.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QComboBox

from src.utils.enums import WhisperModelEnum, WhisperDeviceEnum, SubtitleExtEnum


class SettingsPanel(QWidget):
    def __init__(
        self, logger: logging.Logger, root_dir: str, config: providers.Configuration
    ):
        super().__init__()

        self.logger = logger
        self.root_dir = root_dir
        self.config = config

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        settings_group_box = self.init_settings_ui()

        layout.addWidget(settings_group_box)

    def init_settings_ui(self):
        settings_group_box = QGroupBox("Settings")
        settings_layout = QVBoxLayout()
        settings_group_box.setLayout(settings_layout)

        translator_group_box = self.init_translator_settings_ui()

        settings_layout.addWidget(translator_group_box)

        h_layout = QHBoxLayout()

        audio_extractor_group_box = self.init_audio_extractor_settings_ui()

        h_layout.addWidget(audio_extractor_group_box)

        subtitle_generator_group_box = self.init_subtitle_generator_settings_ui()

        h_layout.addWidget(subtitle_generator_group_box)

        settings_layout.addLayout(h_layout)

        return settings_group_box

    def init_translator_settings_ui(self):
        translator_group_box = QGroupBox("Translator")
        translator_layout = QVBoxLayout()
        
        
        
        translator_group_box.setLayout(translator_layout)

        return translator_group_box

    def init_audio_extractor_settings_ui(self):
        audio_extractor_group_box = QGroupBox("Audio Extractor")
        audio_extractor_layout = QVBoxLayout()
        
        h_layout = QHBoxLayout()

        whisper_model_label = QLabel("Whisper Model")
        h_layout.addWidget(whisper_model_label)
        
        whisper_model_comgo_box = self.init_whisper_model_combobox()
        h_layout.addWidget(whisper_model_comgo_box)
        
        whisper_devide_label = QLabel("Device")
        h_layout.addWidget(whisper_devide_label)
        
        whisper_device_comgo_box = self.init_whisper_device_combobox()
        h_layout.addWidget(whisper_device_comgo_box)

        audio_extractor_layout.addLayout(h_layout)        
        audio_extractor_group_box.setLayout(audio_extractor_layout)

        return audio_extractor_group_box

    def init_whisper_model_combobox(self):
        whisper_model_combo_box = QComboBox()
        
        models = [model.value for model in WhisperModelEnum]
        current_model = self.config["audio_extractor"]["whisper_model"]
        for idx, model in enumerate(models):
            whisper_model_combo_box.addItem(model)
            if model == current_model:
                whisper_model_combo_box.setCurrentIndex(idx)

        return whisper_model_combo_box

    def init_whisper_device_combobox(self):
        whisper_device_combo_box = QComboBox()
        
        devices = [device.value for device in WhisperDeviceEnum]
        current_device = self.config["audio_extractor"]["device"]
        for idx, device in enumerate(devices):
            whisper_device_combo_box.addItem(device)
            if device == current_device:
                whisper_device_combo_box.setCurrentIndex(idx)
                
        return whisper_device_combo_box

    def init_subtitle_generator_settings_ui(self):
        subtitle_generator_group_box = QGroupBox("Subtitle Generator")
        subtitle_generator_layout = QVBoxLayout()
        
        h_layout = QHBoxLayout()
        
        subtitle_ext_label = QLabel("Extension")
        h_layout.addWidget(subtitle_ext_label)
        
        subtitle_ext_comgo_box = self.init_subtitle_ext_combobox()
        h_layout.addWidget(subtitle_ext_comgo_box)
        
        subtitle_generator_layout.addLayout(h_layout)
        subtitle_generator_group_box.setLayout(subtitle_generator_layout)

        return subtitle_generator_group_box

    def init_subtitle_ext_combobox(self):
        subtitle_ext_combo_box = QComboBox()
        
        exts = [ext.value for ext in SubtitleExtEnum]
        current_ext = self.config["subtitle_generator"]["ext"]
        
        for idx, ext in enumerate(exts):
            subtitle_ext_combo_box.addItem(ext)
            if ext == current_ext:
                subtitle_ext_combo_box.setCurrentIndex(idx)
                
        return subtitle_ext_combo_box
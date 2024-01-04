import logging
import os

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
)

from src.utils.enums import AvailableAudioExtEnum, SubtitleExtEnum

class StateSignals(QObject):
    modelChanged = Signal(str)
    extChanged = Signal(str)


class ExecuteLayout(QVBoxLayout):
    def __init__(self, audio_extractor, translator, subtitle_generator):
        super().__init__()
        self.translator = translator
        self.audio_extractor = audio_extractor
        self.subtitle_generator = subtitle_generator

        self.state_signals = StateSignals()
        self.state_signals.modelChanged.connect(self.onModelChanged)
        self.state_signals.extChanged.connect(self.onExtChanged)

        # UI 구성 요소 선언
        self.api_key_label = QLabel()
        self.api_key_lineedit = QLineEdit()
        self.api_key_edit_button = QPushButton("수정")
        self.whisper_model_combo = QComboBox()
        self.subtitle_ext_combo = QComboBox()
        self.execute_button = QPushButton("번역")
        self.log_viewer = QPlainTextEdit()

        self.init_ui()

    def init_ui(self):
        self.init_api_key_layout()
        self.init_execute_layout()
        self.init_log_viewer()

    def init_api_key_layout(self):
        api_key_layout = QHBoxLayout()

        self.api_key_label.setText(f"Deepl API Key: {self.translator.load_api_key()}")
        api_key_layout.addWidget(self.api_key_label)

        api_key_layout.addWidget(self.api_key_lineedit)

        self.api_key_edit_button.clicked.connect(self.edit_api_key)
        api_key_layout.addWidget(self.api_key_edit_button)

        self.addLayout(api_key_layout)

    def init_execute_layout(self):
        execute_layout = QHBoxLayout()

        self.whisper_model_label = QLabel(f"Whisper 모델: {self.audio_extractor.current_model}")
        execute_layout.addWidget(self.whisper_model_label)

        for model in self.audio_extractor.models:
            self.whisper_model_combo.addItem(model)
        self.whisper_model_combo.activated[int].connect(self.set_selected_model)
        execute_layout.addWidget(self.whisper_model_combo)

        self.subtitle_ext_label = QLabel(f"자막 확장자: {self.subtitle_generator.ext}")
        execute_layout.addWidget(self.subtitle_ext_label)

        for ext in [ext.value for ext in SubtitleExtEnum]:
            self.subtitle_ext_combo.addItem(ext)
        self.subtitle_ext_combo.activated[int].connect(self.set_selected_ext)
        execute_layout.addWidget(self.subtitle_ext_combo)

        self.execute_button.clicked.connect(self.execute)
        execute_layout.addWidget(self.execute_button)

        self.addLayout(execute_layout)

    def init_log_viewer(self):
        self.log_viewer.setReadOnly(True)
        self.addWidget(self.log_viewer)
        
        self.log_viewer.setPlainText("Hassan is ready to work!")
        
        self.audio_extractor.set_log_viewer(self.log_viewer)
        self.translator.set_log_viewer(self.log_viewer)
        self.subtitle_generator.set_log_viewer(self.log_viewer)
        

    def edit_api_key(self):
        new_api_key = self.api_key_lineedit.text()
        self.translator.edit_api_key(new_api_key)
        self.api_key_label.setText(f"Deepl API Key: {self.translator.load_api_key()}")

    def init_whisper_model(self):
        current_model = self.audio_extractor.current_model
        self.whisper_model_label.setText(f"Whisper 모델: {current_model}")

    def set_selected_model(self, model_index):
        selected_model = self.audio_extractor.models[model_index]
        logging.info(f"Selected model: {selected_model}")
        self.state_signals.modelChanged.emit(selected_model)

    def onModelChanged(self, model):
        # 모델 변경에 대한 처리 로직
        self.audio_extractor.change_model_config(model)
        self.whisper_model_label.setText(f"Whisper 모델: {model}")

    def init_subtitle_ext(self):
        subtitle_ext = self.subtitle_generator.load_subtitle_ext()
        self.subtitle_ext_label.setText(f"자막 확장자: {subtitle_ext}")

    def set_selected_ext(self, ext_index):
        selected_ext = self.subtitle_generator.subs_exts[ext_index]
        logging.info(f"Selected subtitle extension: {selected_ext}")
        self.state_signals.extChanged.emit(selected_ext)

    def onExtChanged(self, ext):
        # 확장자 변경에 대한 처리 로직
        self.subtitle_generator.edit_subtitle_ext(ext)
        self.subtitle_ext_label.setText(f"자막 확장자: {ext}")

    def execute(self):
        refined_paths = self.path_table.get_removed_redudant_paths()
        
        info_log = "Start execution"
        logging.info(info_log)
        self.log_viewer.appendPlainText(info_log)
        for path in refined_paths:
            if path["type"] == "folder":
                self.execute_folder(path["path"])
            elif path["type"] == "file":
                self.execute_file(path["path"])
        self.path_table.setRowCount(0)
        info_log = "Finished all executions"
        logging.info(info_log)
        self.log_viewer.appendPlainText(info_log)

    def is_available_audio_file(self, file_path):
        ext = os.path.splitext(file_path)[-1]
        return ext in [ext.value for ext in AvailableAudioExtEnum]

    def execute_folder(self, folder_path):
        logging.info(f"Executing {folder_path}")
        try:
            listdir = os.listdir(folder_path)
        except Exception as exc:
            logging.error(f"Failed to execute {folder_path}: {exc}")
            return
        
        audio_files = [
            path
            for path in listdir
            if os.path.isfile(os.path.join(folder_path, path))
            and self.is_available_audio_file(path)
        ]

        folders = [
            path for path in listdir if os.path.isdir(os.path.join(folder_path, path))
        ]

        for audio_file in audio_files:
            self.execute_file(os.path.join(folder_path, audio_file))

        for folder in folders:
            self.execute_folder(os.path.join(folder_path, folder))

    def execute_file(self, file_path):
        logging.info(f"Executing {file_path}")
        extracted_transcription = self.audio_extractor.extract_transcription(file_path)
        translated_transcription = self.translator.translate(
            file_path, extracted_transcription
        )
        self.subtitle_generator.generate_subtitle(file_path, translated_transcription)
        self.log_viewer.appendPlainText(f"Successfully finished {file_path}")
        logging.info(f"Finished {file_path}")


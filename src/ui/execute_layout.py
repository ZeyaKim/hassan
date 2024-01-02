import logging
import os

from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
)


class ExecuteLayout(QVBoxLayout):
    def __init__(self, audio_extractor, translator, subtitle_generator):
        super().__init__()
        self.translator = translator
        self.audio_extractor = audio_extractor
        self.subtitle_generator = subtitle_generator
        self.init_ui()

    def init_ui(self):
        api_key_layout = QHBoxLayout()

        self.api_key_label = QLabel()
        self.api_key_label.setText(f"Deepl API Key: {self.translator.load_api_key()}")
        api_key_layout.addWidget(self.api_key_label)

        self.api_key_lineedit = QLineEdit()
        api_key_layout.addWidget(self.api_key_lineedit)

        self.api_key_edit_button = QPushButton("수정")
        self.api_key_edit_button.clicked.connect(self.edit_api_key)
        api_key_layout.addWidget(self.api_key_edit_button)

        self.addLayout(api_key_layout)

        execute_layout = QHBoxLayout()

        self.whisper_model_label = QLabel()
        self.whisper_model_label.setText(
            f"Whisper 모델: {self.audio_extractor.current_model}"
        )
        execute_layout.addWidget(self.whisper_model_label)

        self.whisper_model_combo = QComboBox(self)
        for model in self.audio_extractor.models:
            self.whisper_model_combo.addItem(model)
        self.whisper_model_combo.activated[int].connect(self.set_selected_model)
        execute_layout.addWidget(self.whisper_model_combo)

        self.whisper_model_edit_button = QPushButton("Whisper 모델 변경", self)
        self.whisper_model_edit_button.clicked.connect(self.edit_whisper_model)
        execute_layout.addWidget(self.whisper_model_edit_button)

        self.subtitle_ext_label = QLabel()
        self.subtitle_ext_label.setText(f"자막 확장자: {self.subtitle_generator.ext}")
        execute_layout.addWidget(self.subtitle_ext_label)

        self.subtitle_ext_combo = QComboBox(self)
        for ext in self.subtitle_generator.subs_exts:
            self.subtitle_ext_combo.addItem(ext)
        self.subtitle_ext_combo.activated[int].connect(self.set_selected_ext)
        execute_layout.addWidget(self.subtitle_ext_combo)

        self.subtitle_ext_edit_button = QPushButton("자막 확장자 변경", self)
        self.subtitle_ext_edit_button.clicked.connect(self.edit_subtitle_ext)
        execute_layout.addWidget(self.subtitle_ext_edit_button)

        self.execute_button = QPushButton("번역", self)
        self.execute_button.clicked.connect(self.execute)
        execute_layout.addWidget(self.execute_button)

        self.addLayout(execute_layout)

        self.info_log_viewer = QPlainTextEdit(self)
        self.info_log_viewer.setReadOnly(True)
        self.addWidget(self.info_log_viewer)

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
        self.selected_model = selected_model

    def edit_whisper_model(self):
        self.audio_extractor.change_model_config(self.selected_model)
        self.whisper_model_label.setText(
            f"Whisper 모델: {self.audio_extractor.current_model}"
        )

    def init_subtitle_ext(self):
        subtitle_ext = self.subtitle_generator.load_subtitle_ext()
        self.subtitle_ext_label.setText(f"자막 확장자: {subtitle_ext}")

    def set_selected_ext(self, ext_index):
        selected_ext = self.subtitle_generator.subs_exts[ext_index]
        logging.info(f"Selected subtitle extension: {selected_ext}")
        self.selected_ext = selected_ext

    def edit_subtitle_ext(self):
        self.subtitle_generator.edit_subtitle_ext(self.selected_ext)
        self.subtitle_ext_label.setText(f"자막 확장자: {self.subtitle_generator.ext}")

    def execute(self):
        refined_paths = self.path_table.get_removed_redudant_paths()
        for path in refined_paths:
            if path["type"] == "folder":
                self.execute_folder(path["path"])
            elif path["type"] == "file":
                self.execute_file(path["path"])
        self.path_table.setRowCount(0)

    def execute_folder(self, folder_path):
        logging.info(f"Executing {folder_path}")
        listdir = os.listdir(folder_path)

        audio_files = [
            path
            for path in listdir
            if os.path.isfile(os.path.join(folder_path, path))
            and path.split(".")[-1] in ["mp3", "wav"]
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
        logging.info(f"Finished {file_path}")

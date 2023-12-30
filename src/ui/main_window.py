import logging

from src.translator import Translator
from PySide6.QtWidgets import (QFileDialog, QLabel, QLineEdit, QListWidget,
                               QMainWindow, QPlainTextEdit, QPushButton,
                               QVBoxLayout, QWidget)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.translator = Translator()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Work Hard Hassan!")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.add_file_paths_button = QPushButton("파일 추가", self)
        self.add_file_paths_button.clicked.connect(self.add_file_paths)
        layout.addWidget(self.add_file_paths_button)

        self.add_folder_paths_button = QPushButton("폴더 추가", self)
        self.add_folder_paths_button.clicked.connect(self.add_folder_paths)
        layout.addWidget(self.add_folder_paths_button)

        self.added_paths_list = QListWidget(self)
        layout.addWidget(self.added_paths_list)

        self.api_key_label = QLabel()
        self.init_api_key_label()
        layout.addWidget(self.api_key_label)

        self.api_key_lineedit = QLineEdit(self)
        layout.addWidget(self.api_key_lineedit)

        self.api_key_edit_button = QPushButton("수정", self)
        self.api_key_edit_button.clicked.connect(self.change_api_key)
        layout.addWidget(self.api_key_edit_button)

        self.execute_button = QPushButton("실행", self)
        layout.addWidget(self.execute_button)

        self.progress_log_viewer = QPlainTextEdit(self)
        self.progress_log_viewer.setReadOnly(True)
        layout.addWidget(self.progress_log_viewer)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_file_paths(self):
        file_dialog = QFileDialog(self)
        file_paths = file_dialog.getOpenFileNames(
            self, "Select Audio Files", "", "Audio Files (*.mp3 *.wav)"
        )

        added_paths = [
            self.added_paths_list.item(i).text()
            for i in range(self.added_paths_list.count())
        ]

        for selected_file_path in file_paths[0]:
            if selected_file_path in added_paths:
                logging.info(f"{selected_file_path} is already added")
                continue
            else:
                self.added_paths_list.addItem(selected_file_path)
                logging.info(f"{selected_file_path} is added")

    def add_folder_paths(self):
        folder_dialog = QFileDialog(self)
        selected_folder_path = folder_dialog.getExistingDirectory(self, "Select Folder")

        added_paths = [
            self.added_paths_list.item(i).text()
            for i in range(self.added_paths_list.count())
        ]

        if selected_folder_path in added_paths:
            logging.info(f"{selected_folder_path} is already added")
        else:
            self.added_paths_list.addItem(selected_folder_path)
            logging.info(f"{selected_folder_path} is added")

    def is_valid_api_key(self, api_key):
        return True
    
    def change_api_key(self):
        new_api_key = self.api_key_lineedit.text()
        if self.is_valid_api_key(new_api_key):
            self.api_key = new_api_key
            self.init_api_key_label()
            
    def init_api_key_label(self):
        api_key = self.translator.api_key
        self.api_key_label.setText(f"API Key: {api_key}")
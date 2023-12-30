
from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from src.translator import Translator
from .path_list import PathList

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

        self.path_list = PathList()
        layout.addWidget(self.path_list)

        self.api_key_label = QLabel()
        self.init_api_key_label()
        layout.addWidget(self.api_key_label)

        self.api_key_lineedit = QLineEdit(self)
        layout.addWidget(self.api_key_lineedit)

        self.api_key_edit_button = QPushButton("수정", self)
        self.api_key_edit_button.clicked.connect(self.change_api_key)
        layout.addWidget(self.api_key_edit_button)

        self.execute_button = QPushButton("번역", self)
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

        for selected_file_path in file_paths[0]:
            self.path_list.add_new_path(selected_file_path)

    def add_folder_paths(self):
        folder_dialog = QFileDialog(self)
        selected_folder_path = folder_dialog.getExistingDirectory(self, "Select Folder")

        self.path_list.add_new_path(selected_folder_path)

    def change_api_key(self):
        new_api_key = self.api_key_lineedit.text()
        self.translator.edit_api_key(new_api_key)
        self.api_key_label.setText(f"API Key: {self.translator.load_api_key()}")

    def init_api_key_label(self):
        api_key = self.translator.load_api_key()
        self.api_key_label.setText(f"API Key: {api_key}")

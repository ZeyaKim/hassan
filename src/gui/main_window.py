import pathlib

from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QListView,
    QFileDialog,
    QHBoxLayout,
    QDialog,
    QLabel,
    QLineEdit,
)
from PyQt5.QtCore import QStringListModel, Qt
from src.services.paths_storage import PathsStorage
from src.services.process_handler import ProcessHandler
from src.services.translator import Translator


class MainWindow(QMainWindow):
    def __init__(
        self,
        paths_storage: PathsStorage,
        process_handler: ProcessHandler,
        translator: Translator,
    ):
        super().__init__()
        self.paths_storage = paths_storage
        self.process_handler = process_handler
        self.translator = translator
        self.setup_ui()

        self.process_handler.finished.connect(self.on_finished)
        self.translator.api_key_changed.connect(self.api_key_changed)

    def setup_ui(self):
        self.setWindowTitle("Hassan")
        self.setGeometry(100, 100, 800, 600)

        add_files_button = QPushButton("Add Files")
        add_folder_button = QPushButton("Add Folders")

        add_files_button.clicked.connect(self.add_files)
        add_folder_button.clicked.connect(self.add_folder)

        set_api_key_button = QPushButton("Set API Key")
        set_api_key_button.clicked.connect(self.set_api_key)

        self.paths_viewer = QListView()
        self.string_list_model = QStringListModel()

        self.paths_viewer.setModel(self.string_list_model)

        self.is_running_label = QLabel("Process is not running")
        self.is_running_label.setAlignment(Qt.AlignCenter)

        run_button = QPushButton("Run")
        run_button.clicked.connect(lambda: self.run())

        # 레이아웃 생성 및 버튼 추가
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        h_layout.addWidget(add_files_button)  # 레이아웃에 'Add Files' 버튼 추가
        h_layout.addWidget(add_folder_button)  # 레이아웃에 'Add Folders' 버튼 추가
        h_layout.addWidget(set_api_key_button)

        v_layout.addLayout(h_layout)  # 레이아웃에 h_layout 추가
        v_layout.addWidget(self.paths_viewer)
        v_layout.addWidget(self.is_running_label)
        v_layout.addWidget(run_button)

        # 중앙 위젯 생성 및 레이아웃 설정
        central_widget = QWidget()  # 중앙 위젯 생성
        central_widget.setLayout(v_layout)  # 중앙 위젯에 레이아웃 설정
        self.setCentralWidget(central_widget)  # 메인 윈도우의 중앙 위젯으로 설정

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Open Media File",
            "",
            "Audio Files (*.mp3 *.wav);;Video Files (*.mp4)",
        )

        for file in files:
            self.paths_storage.add_path(pathlib.Path(file))

        self.string_list_model.setStringList(
            [str(file) for file in self.paths_storage.file_paths]
            + [str(folder) for folder in self.paths_storage.folder_paths]
        )

    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Open Media Folder")
        self.paths_storage.add_path(pathlib.Path(folder))

        self.string_list_model.setStringList(
            [str(file) for file in self.paths_storage.file_paths]
            + [str(folder) for folder in self.paths_storage.folder_paths]
        )

    def set_api_key(self):
        self.set_api_key_dialog = QDialog()
        self.set_api_key_dialog.setWindowTitle("Set API Key")
        self.set_api_key_dialog.setGeometry(100, 100, 400, 100)

        layout = QVBoxLayout()

        current_api_key_label = QLabel(
            f"Current API Key: {self.translator.get_masked_api_key()}"
        )
        layout.addWidget(current_api_key_label)

        api_key_input = QLineEdit()
        layout.addWidget(api_key_input)

        self.set_api_key_button = QPushButton("Set")
        self.set_api_key_button.clicked.connect(
            lambda: self.translator.set_api_key(api_key_input.text())
        )
        layout.addWidget(self.set_api_key_button)

        self.set_api_key_dialog.setLayout(layout)

        self.set_api_key_dialog.exec_()

    def run(self):
        self.is_running_label.setText("Process is running")
        self.process_handler.run()

    def on_finished(self):
        self.is_running_label.setText("Process is not running")

    def api_key_changed(self):
        self.set_api_key_dialog.close()

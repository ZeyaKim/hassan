import pathlib

from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QListView,
    QFileDialog,
)
from PyQt5.QtCore import QStringListModel
from src.services.paths_storage import PathsStorage
from src.services.process_handler import ProcessHandler


class MainWindow(QMainWindow):
    def __init__(self, paths_storage: PathsStorage, process_handler: ProcessHandler):
        super().__init__()
        self.paths_storage = paths_storage
        self.process_handler = process_handler
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Hello World")
        self.setGeometry(100, 100, 800, 600)

        add_files_button = QPushButton("Add Files")
        add_folder_button = QPushButton("Add Folders")

        add_files_button.clicked.connect(self.add_files)
        add_folder_button.clicked.connect(self.add_folder)

        self.paths_viewer = QListView()
        self.string_list_model = QStringListModel()

        self.paths_viewer.setModel(self.string_list_model)

        run_button = QPushButton("Run")
        run_button.clicked.connect(self.run)

        # 레이아웃 생성 및 버튼 추가
        layout = (
            QVBoxLayout()
        )  # 버튼들을 수직으로 정렬하기 위한 QVBoxLayout 인스턴스 생성
        layout.addWidget(add_files_button)  # 레이아웃에 'Add Files' 버튼 추가
        layout.addWidget(add_folder_button)  # 레이아웃에 'Add Folders' 버튼 추가
        layout.addWidget(self.paths_viewer)
        layout.addWidget(run_button)

        # 중앙 위젯 생성 및 레이아웃 설정
        central_widget = QWidget()  # 중앙 위젯 생성
        central_widget.setLayout(layout)  # 중앙 위젯에 레이아웃 설정
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

    def run(self):
        self.process_handler.run()

from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QMenu,
    QPushButton,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from src.audio_extractor import AudioExtractor
from src.subtitle_generator import SubtitleGenerator
from src.translator import Translator

from .execute_layout import ExecuteLayout
from .path_table import PathTable


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.translator = Translator()
        self.audio_extractor = AudioExtractor()
        self.subtitle_generator = SubtitleGenerator()
        self.setWindowIcon(QIcon("assets/icon/hassan_icon.png"))

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Work Hard Hassan!")
        self.setGeometry(100, 100, 1080, 720)

        layout = QVBoxLayout()

        path_button_layout = QHBoxLayout()

        self.add_file_paths_button = QPushButton("파일 추가", self)
        self.add_file_paths_button.clicked.connect(self.add_file_paths)
        path_button_layout.addWidget(self.add_file_paths_button)

        self.add_folder_paths_button = QPushButton("폴더 추가", self)
        self.add_folder_paths_button.clicked.connect(self.add_folder_paths)
        path_button_layout.addWidget(self.add_folder_paths_button)

        layout.addLayout(path_button_layout)

        self.path_table = PathTable()
        layout.addWidget(self.path_table)

        execute_setting_layout = ExecuteLayout(
            self.audio_extractor, self.translator, self.subtitle_generator
        )

        layout.addLayout(execute_setting_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.create_tray_icon()

    def add_file_paths(self):
        file_dialog = QFileDialog(self)
        file_paths = file_dialog.getOpenFileNames(
            self, "Select Audio Files", "", "Audio Files (*.mp3 *.wav)"
        )

        for selected_file_path in file_paths[0]:
            self.path_table.add_new_path(selected_file_path, path_type="file")

    def add_folder_paths(self):
        folder_dialog = QFileDialog(self)
        selected_folder_path = folder_dialog.getExistingDirectory(self, "Select Folder")

        self.path_table.add_new_path(selected_folder_path, path_type="folder")

    def create_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("assets/icon/hassan_icon.png"))

        tray_menu = QMenu()
        show_action = QAction("보기", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)

        exit_action = QAction("종료", self)
        exit_action.triggered.connect(QApplication.instance().quit)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def closeEvent(self, event):
        if QApplication.activeWindow() is not None:
            # 애플리케이션이 활성 상태일 때만 메시지를 출력
            self.tray_icon.showMessage(
                "Work Hard Hassan!", "하산이 야근하고 있습니다!", QSystemTrayIcon.Information, 2000
            )
        event.ignore()
        self.hide()

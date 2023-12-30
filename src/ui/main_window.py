from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QPlainTextEdit,
    QPushButton,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from src.translator import Translator

from .path_table import PathTable


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.translator = Translator()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Work Hard Hassan!")
        self.setGeometry(100, 100, 1080, 720)

        layout = QVBoxLayout()

        self.add_file_paths_button = QPushButton("파일 추가", self)
        self.add_file_paths_button.clicked.connect(self.add_file_paths)
        layout.addWidget(self.add_file_paths_button)

        self.add_folder_paths_button = QPushButton("폴더 추가", self)
        self.add_folder_paths_button.clicked.connect(self.add_folder_paths)
        layout.addWidget(self.add_folder_paths_button)

        self.path_table = PathTable()
        layout.addWidget(self.path_table)

        self.api_key_label = QLabel()
        self.init_api_key_label()
        layout.addWidget(self.api_key_label)

        self.api_key_lineedit = QLineEdit(self)
        layout.addWidget(self.api_key_lineedit)

        self.api_key_edit_button = QPushButton("수정", self)
        self.api_key_edit_button.clicked.connect(self.edit_api_key)
        layout.addWidget(self.api_key_edit_button)

        self.execute_button = QPushButton("번역", self)
        self.execute_button.clicked.connect(self.execute)
        layout.addWidget(self.execute_button)

        self.progress_log_viewer = QPlainTextEdit(self)
        self.progress_log_viewer.setReadOnly(True)
        layout.addWidget(self.progress_log_viewer)

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

    def edit_api_key(self):
        new_api_key = self.api_key_lineedit.text()
        self.translator.edit_api_key(new_api_key)
        self.api_key_label.setText(f"API Key: {self.translator.load_api_key()}")

    def init_api_key_label(self):
        api_key = self.translator.load_api_key()
        self.api_key_label.setText(f"API Key: {api_key}")

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
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Work Hard Hassan!", "하산이 야근하고 있습니다!", QSystemTrayIcon.Information, 2000
        )

    def execute(self):
        self.path_table.get_removed_redudant_paths()
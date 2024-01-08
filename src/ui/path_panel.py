import logging

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QMenu,
    QPlainTextEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)


class PathPanel(QVBoxLayout):
    def __init__(self, log_viewer: QPlainTextEdit) -> None:
        super().__init__()
        self.log_viewer = log_viewer
        self.init_ui()

    def init_ui(self) -> None:
        self.add_files_button, self.add_folder_button = self.init_path_buttons()
        self.path_viewer = self.init_path_viewer()

    def init_path_buttons(self) -> tuple[QPushButton, QPushButton]:
        buttons_layout = QHBoxLayout()

        add_file_paths_button = QPushButton("파일 추가")
        add_file_paths_button.clicked.connect(self.add_file_paths)

        add_folder_path_button = QPushButton("폴더 추가")
        add_folder_path_button.clicked.connect(self.add_folder_path)

        buttons_layout.addWidget(add_file_paths_button)
        buttons_layout.addWidget(add_folder_path_button)

        self.addLayout(buttons_layout)

        return add_file_paths_button, add_folder_path_button

    def init_path_viewer(self) -> QTableWidget:
        path_viewer = QTableWidget()
        path_viewer.setColumnCount(2)
        path_viewer.setHorizontalHeaderLabels(["경로", "타입"])
        path_viewer.setContextMenuPolicy(Qt.CustomContextMenu)
        path_viewer.customContextMenuRequested.connect(self.show_delete_menu)

        header = path_viewer.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        path_viewer.setColumnWidth(1, 100)

        self.addWidget(path_viewer)

        return path_viewer

    def show_delete_menu(self, position) -> None:
        menu = QMenu(self)
        delete_action = QAction("삭제", self)
        menu.addAction(delete_action)

        action = menu.exec(self.mapToGlobal(position))

        if action == delete_action:
            selected_row = self.currentRow()
            if selected_row != -1:
                self.removeRow(selected_row)
                
    def categorize_paths(self, paths) -> tuple[set[str], set[str]]:
        folders, files = set(), set()
        for path, path_type in paths:
            match path_type:
                case "folder":
                    folders.add(path)
                case "file":
                    files.add(path)
        return folders, files

    def refine_paths(self) -> dict[str, list[str]]:
        folders, files = self.categorize_paths()

        unique_folders: set[str] = set()

        for folder in sorted(folders, key=len):
            if not any(
                folder.startswith(other_folder) for other_folder in unique_folders
            ):
                unique_folders.add(folder)

        unique_files: set[str] = {
            file
            for file in files
            if not any(file.startswith(folder) for folder in unique_folders)
        }

        return {"folders": list(unique_folders), "files": list(unique_files)}

    @Slot()
    def add_file_paths(self) -> None:
        with QFileDialog(self) as file_dialog:
            file_paths = file_dialog.getOpenFileNames(self, "Select Audio Files", "", "Audio Files (*.mp3 *.wav)")
            
            for file_path in file_paths[0]:
                self.add_path_item(file_path, "file")

    @Slot()
    def add_folder_path(self) -> None:
        with QFileDialog(self) as folder_dialog:
            selected_folder_path = folder_dialog.getExistingDirectory(self, "Select Folder")

            self.add_path_item(selected_folder_path, "folder")

    def add_path_item(self, path, path_type) -> None:
        if self.is_already_added(path):
            info_msg: str = f"{path} is already added"
        else:
            rowCount: int = self.path_viewer.rowCount()
            self.path_viewer.insertRow(rowCount)
            self.path_viewer.setItem(rowCount, 0, QTableWidgetItem(path))
            self.path_viewer.setItem(rowCount, 1, QTableWidgetItem(path_type))
            info_msg: str = f"{path} is added"

            logging.info(info_msg)
            self.log_viewer.appendPlainText(info_msg)

    def is_already_added(self, path) -> bool:
        return any(
            self.path_viewer.item(idx.row(), 0).text() == path
            for idx in range(self.path_viewer.rowCount())
        )

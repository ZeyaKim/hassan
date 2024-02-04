from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QHeaderView,
    QMenu,
    QTableWidget,
    QTableWidgetItem,
)

from src.utils import enums


class PathViewer(QTableWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["Name", "Path", "Type"])

        self.setColumnWidth(0, 300)

        header = self.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        self.setColumnWidth(2, 100)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_delete_menu)

    def show_delete_menu(self, pos):
        menu = QMenu(self)
        delete_action = menu.addAction("Delete")

        action = menu.exec_(self.mapToGlobal(pos))

        if action == delete_action:
            selected_row = self.currentRow()
            deleted_path = self.item(selected_row, 1).text()

            self.removeRow(selected_row)

            self.logger.info(f"Path {deleted_path} is deleted")

    def add_file_paths(self):
        available_exts = ["*" + ext.value for ext in enums.ExtractableExtEnum]
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Audio Files",
            filter=f"Audio Files ({' '.join(available_exts)})",
        )

        if file_paths:
            for file_path in file_paths:
                self.add_path_item(file_path, "File")

    def add_folder_paths(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.add_path_item(folder_path, "Folder")

    def add_path_item(self, path, path_type):
        if self.is_path_exist(path):
            self.logger.info(f"{path} is already exist")
            return

        row = self.rowCount()
        self.insertRow(row)

        name = path.split("/")[-1]
        row_info = [name, path, path_type]

        for idx, info in enumerate(row_info):
            item = QTableWidgetItem(info)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.setItem(row, idx, item)
        self.logger.info(f"Added {path}")

    def is_path_exist(self, path: str):
        return any(self.item(row, 1).text() == path for row in range(self.rowCount()))

    def get_paths(self):
        return [
            {
                "path": self.item(row, 1).text(),
                "type": self.item(row, 2).text(),
            }
            for row in range(self.rowCount())
        ]

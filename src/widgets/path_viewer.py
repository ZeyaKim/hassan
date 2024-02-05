import os
import logging

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
    """
    A custom table widget for displaying and managing file and folder paths.

    Attributes:
        logger: The logger object for logging messages.
        path_info: A dictionary that stores the path information.

    Methods:
        init_ui: Initializes the user interface of the table widget.
        show_delete_menu: Displays a context menu for deleting a path.
        add_file_paths: Opens a file dialog to select and add file paths.
        add_folder_paths: Opens a folder dialog to select and add folder paths.
        add_path_item: Adds a path item to the table widget.
        is_path_exist: Checks if a path already exists in the path_info dictionary.
        get_paths: Returns a list of paths and their types from the path_info dictionary.
        add_path_in_map: Adds a path and its type to the path_info dictionary.
        remove_path_in_map: Removes a path from the path_info dictionary.
    """

    def __init__(self, logger: logging.Logger):
        super().__init__()
        self.init_ui()
        self.logger = logger
        self.path_info = dict()

    def init_ui(self) -> None:
        """
        Initializes the user interface of the table widget.
        """
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["Name", "Path", "Type"])

        self.setColumnWidth(0, 300)

        header = self.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        self.setColumnWidth(2, 100)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_delete_menu)

    def show_delete_menu(self, pos) -> None:
        """
        Displays a context menu for deleting a path.

        Args:
            pos: The position of the context menu.

        """
        menu = QMenu(self)
        delete_action = menu.addAction("Delete")

        action = menu.exec_(self.mapToGlobal(pos))

        if action == delete_action:
            selected_row = self.currentRow()
            deleted_path = self.item(selected_row, 1).text()

            self.removeRow(selected_row)
            self.remove_path_in_map(deleted_path)
            self.logger.info(f"Path {deleted_path} is deleted")

    def add_file_paths(self) -> None:
        """
        Opens a file dialog to select and add file paths.
        """
        available_exts = ["*" + ext.value for ext in enums.ExtractableExtEnum]
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Audio Files",
            filter=f"Audio Files ({' '.join(available_exts)})",
        )

        if file_paths:
            for file_path in file_paths:
                self.add_path_item(file_path, "File")

    def add_folder_paths(self) -> None:
        """
        Opens a folder dialog to select and add folder paths.
        """
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.add_path_item(folder_path, "Folder")

    def add_path_item(self, path: str, path_type: str) -> None:
        """
        Adds a path item to the table widget.

        Args:
            path: The path to be added.
            path_type: The type of the path (File or Folder).
        """
        if self.is_path_exist(path):
            self.logger.info(f"{path} is already exist")
            return

        row = self.rowCount()
        self.insertRow(row)

        path = os.path.normpath(path)
        name = os.path.basename(path)
        row_info = [name, path, path_type]

        for idx, info in enumerate(row_info):
            item = QTableWidgetItem(info)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.setItem(row, idx, item)

        self.add_path_in_map(path, path_type)
        self.logger.info(f"Added {path}")

    def is_path_exist(self, path: str) -> bool:
        """
        Checks if a path already exists in the path_info dictionary.

        Args:
            path: The path to be checked.

        Returns:
            True if the path exists, False otherwise.
        """
        return path in self.path_info.keys()

    def get_paths(self) -> list[tuple[str, str]]:
        """
        Returns a list of paths and their types from the path_info dictionary.

        Returns:
            A list of tuples containing the path and its type.
        """
        return [(path, path_type) for path, path_type in self.path_info.items()]

    def add_path_in_map(self, path: str, path_type: str) -> None:
        """
        Adds a path and its type to the path_info dictionary.

        Args:
            path: The path to be added.
            path_type: The type of the path (File or Folder).
        """
        self.path_info[path] = path_type

    def remove_path_in_map(self, path: str) -> None:
        """
        Removes a path from the path_info dictionary.

        Args:
            path: The path to be removed.
        """
        self.path_info.pop(path)
        
    def on_finished(self):
        self.setRowCount(0)
        self.path_info.clear()
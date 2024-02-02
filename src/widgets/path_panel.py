import logging

from PySide6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import Qt

from utils import enums


class PathPanel(QWidget):
    def __init__(self, logger: logging.Logger, root_dir: str):
        super().__init__()
        self.logger = logger
        self.root_dir = root_dir

        self.init_ui()

    def init_ui(self):
        h_layout = QHBoxLayout()

        path_adder_layout = QVBoxLayout()

        path_adder_group = QGroupBox("Add path")
        path_adder_group.setLayout(path_adder_layout)

        button_1 = QPushButton("Add Files")
        button_1.clicked.connect(self.add_file_paths)
        path_adder_layout.addWidget(button_1)

        button_2 = QPushButton("Add Folder")
        button_2.clicked.connect(self.add_folder_paths)
        path_adder_layout.addWidget(button_2)

        h_layout.addWidget(path_adder_group)

        path_viewer_label = QLabel("Paths")
        self.path_viewer = self.init_path_viewer()

        path_viewer_layout = QVBoxLayout()

        path_viewer_layout.addWidget(path_viewer_label)
        path_viewer_layout.addWidget(self.path_viewer)

        h_layout.addLayout(path_viewer_layout)

        self.setLayout(h_layout)

    def init_path_viewer(self):
        path_viewer = QTableWidget()
        path_viewer.setColumnCount(3)
        path_viewer.setHorizontalHeaderLabels(["Name", "Path", "Type"])

        path_viewer.setColumnWidth(0, 300)  # 첫 번째 열의 너비

        header = path_viewer.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        path_viewer.setColumnWidth(2, 100)  # 세 번째 열의 너비

        return path_viewer

    def add_file_paths(self):
        available_exts = ["*" + ext.value for ext in enums.ExtractableExtEnum]
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Audio Files", filter=f"Audio Files ({' '.join(available_exts)})"
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

        row = self.path_viewer.rowCount()
        self.path_viewer.insertRow(row)

        name = path.split("/")[-1]
        row_info = [name, path, path_type]

        for idx, info in enumerate(row_info):
            item = QTableWidgetItem(info)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.path_viewer.setItem(row, idx, item)
        self.logger.info(f"Added {path}")

    def is_path_exist(self, path):
        return any(
            self.path_viewer.item(row, 1).text() == path
            for row in range(self.path_viewer.rowCount())
        )

    def show_delete_menu(self, pos):
        pass
import logging

from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.widgets import path_viewer


class PathPanel(QWidget):
    def __init__(
        self, logger: logging.Logger, root_dir: str, path_viewer: path_viewer.PathViewer
    ):
        super().__init__()
        self.logger = logger
        self.root_dir = root_dir
        self.path_viewer = path_viewer

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

        path_viewer_layout = QVBoxLayout()

        path_viewer_layout.addWidget(path_viewer_label)
        path_viewer_layout.addWidget(self.path_viewer)

        h_layout.addLayout(path_viewer_layout)

        self.setLayout(h_layout)

import logging

from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)


class PathPanel(QWidget):
    def __init__(self, logger: logging.Logger, root_dir: str):
        super().__init__()
        self.logger = logger
        self.root_dir = root_dir

        self.logger.debug("Initializing path panel")

        self.init_ui()

    def init_ui(self):
        h_layout = QHBoxLayout()

        path_adder_layout = QVBoxLayout()

        path_adder_group = QGroupBox("Add path")
        path_adder_group.setLayout(path_adder_layout)

        button_1 = QPushButton("Add Files")
        path_adder_layout.addWidget(button_1)

        button_2 = QPushButton("Add Folder")
        path_adder_layout.addWidget(button_2)

        h_layout.addWidget(path_adder_group)

        path_viewer_label = QLabel("Paths")
        path_viewer = QTableWidget()

        path_viewer_layout = QVBoxLayout()

        path_viewer_layout.addWidget(path_viewer_label)
        path_viewer_layout.addWidget(path_viewer)

        h_layout.addLayout(path_viewer_layout)

        self.setLayout(h_layout)

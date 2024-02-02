import logging
import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from widgets.path_panel import PathPanel
from widgets.settings_panel import SettingsPanel
from widgets.task_runner_panel import TaskRunnerPanel


class MainWindow(QMainWindow):
    def __init__(
        self,
        logger: logging.Logger,
        root_dir: str,
        path_panel: PathPanel,
        settings_panel: SettingsPanel,
        task_runner_panel: TaskRunnerPanel,
    ):
        super().__init__()

        self.logger = logger
        self.root_dir = root_dir

        self.logger.info("Initializing main window")

        self.path_panel = path_panel
        self.settings_panel = settings_panel
        self.task_runner_panel = task_runner_panel

        self.init_ui()

        self.setWindowIcon(QIcon(os.path.join(root_dir, "assets", "hassan_icon.ico")))

    def init_ui(self):
        self.setWindowTitle("Hassan")
        self.resize(1080, 720)

        main_layout = QVBoxLayout()

        path_panel = self.path_panel
        main_layout.addWidget(path_panel)

        settings_panel = self.settings_panel
        main_layout.addWidget(settings_panel)

        main_layout.addWidget(self.task_runner_panel)

        h_layout = QHBoxLayout()

        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        h_layout.addSpacerItem(spacer)

        exit_button = QPushButton("Exit")
        h_layout.addWidget(exit_button)

        main_layout.addLayout(h_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

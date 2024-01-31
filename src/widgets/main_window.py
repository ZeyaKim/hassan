import logging

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy

from widgets.path_panel import PathPanel
from widgets.settings_panel import SettingsPanel
from widgets.task_runner_panel import TaskRunnerPanel


class MainWindow(QMainWindow):
    def __init__(self, logger: logging.Logger, root_dir: str):
        super().__init__()

        self.logger = logger
        self.root_dir = root_dir

        self.logger.debug("Initializing main window")

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Hassan")
        self.resize(800, 600)

        main_layout = QVBoxLayout()

        path_panel = PathPanel(self.logger, self.root_dir)
        main_layout.addWidget(path_panel)

        settings_panel = SettingsPanel(self.logger, self.root_dir)
        main_layout.addWidget(settings_panel)

        task_runner_panel = TaskRunnerPanel(self.logger, self.root_dir)
        main_layout.addWidget(task_runner_panel)
        
        h_layout = QHBoxLayout()
        
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        h_layout.addSpacerItem(spacer)
        
        exit_button = QPushButton("Exit")
        h_layout.addWidget(exit_button)
        
        main_layout.addLayout(h_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

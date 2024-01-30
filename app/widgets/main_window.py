import logging

from PySide6.QtWidgets import QMainWindow


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
import logging

from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self, logger: logging.Logger, root_dir: str):
        super().__init__()
        self.logger = logger
        self.root_dir = root_dir

        self.logger.info("Initializing main window")
        print(self.root_dir)

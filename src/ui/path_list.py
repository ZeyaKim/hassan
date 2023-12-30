import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QListWidget, QMenu


class PathList(QListWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def add_new_path(self, new_path):
        paths = [self.item(i).text() for i in range(self.count())]
        if new_path not in paths:
            self.addItem(new_path)
            logging.info(f"Path {new_path} is added")
        else:
            logging.info(f"Path {new_path} is already added")

    def get_refined_paths(self):
        ...

    def show_context_menu(self, position):
        menu = QMenu()
        
        delete_action = QAction("삭제", self)
        menu.addAction(delete_action)

        action = menu.exec(self.mapToGlobal(position))

        if action == delete_action:
            selected_item = self.currentItem()
            if selected_item:
                self.takeItem(self.row(selected_item))

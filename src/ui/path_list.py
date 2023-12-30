from PySide6.QtWidgets import QListWidget
import logging

class PathList(QListWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        ...
    
    def add_new_path(self, new_path):
        paths = [self.item(i).text() for i in range(self.count())]
        if new_path not in paths:
            self.addItem(new_path)
            logging.info(f"Path {new_path} is added")
        else:
            logging.info(f"Path {new_path} is already added")
        
    def get_refined_paths(self):
        ...
    
from PySide6.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Work Hard Hassan!')
        self.setGeometry(100, 100, 800, 600)
        
        ...




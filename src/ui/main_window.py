from PySide6.QtWidgets import (QListWidget, QMainWindow, QPushButton,
                               QVBoxLayout, QWidget, QPlainTextEdit)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.paths = []

    def init_ui(self):
        self.setWindowTitle("Work Hard Hassan!")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.add_path_button = QPushButton("경로 추가", self)
        self.add_path_button.clicked.connect(self.add_path)
        layout.addWidget(self.add_path_button)

        self.added_paths_list = QListWidget(self)
        layout.addWidget(self.added_paths_list)
        
        self.execute_button = QPushButton("실행", self)
        layout.addWidget(self.execute_button)

        self.progress_log_viewer = QPlainTextEdit(self)
        self.progress_log_viewer.setReadOnly(True)
        layout.addWidget(self.progress_log_viewer)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        for i in range(20):
            self.progress_log_viewer.appendPlainText(f"{i}번째 줄")
        
    def add_path(self):
        pass

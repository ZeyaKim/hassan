from PySide6.QtWidgets import (QListWidget, QMainWindow, QPushButton, QPlainTextEdit, QLineEdit, QVBoxLayout, QWidget, QLabel, QFileDialog)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.paths = []
        self.api_key = ''
        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Work Hard Hassan!")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.add_file_paths_button = QPushButton("파일 추가", self)
        self.add_file_paths_button.clicked.connect(self.add_file_paths)
        layout.addWidget(self.add_file_paths_button)
        
        self.add_folder_paths_button = QPushButton("폴더 추가", self)
        self.add_folder_paths_button.clicked.connect(self.add_folder_paths)
        layout.addWidget(self.add_folder_paths_button)

        self.added_paths_list = QListWidget(self)
        layout.addWidget(self.added_paths_list)

        self.api_key_label = QLabel(f"API Key: {self.api_key}", self)
        layout.addWidget(self.api_key_label)
        
        self.api_key_lineedit = QLineEdit(self)
        layout.addWidget(self.api_key_lineedit)
        
        self.api_key_edit_button = QPushButton("수정", self)
        layout.addWidget(self.api_key_edit_button)
        
        self.execute_button = QPushButton("실행", self)
        layout.addWidget(self.execute_button)

        self.progress_log_viewer = QPlainTextEdit(self)
        self.progress_log_viewer.setReadOnly(True)
        layout.addWidget(self.progress_log_viewer)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
    def add_file_paths(self):
        file_dialog = QFileDialog(self)
        file_paths = file_dialog.getOpenFileNames(self, "Select Audio Files", "", "Audio Files (*.mp3 *.wav)")
        print(file_paths[0])
        
    def add_folder_paths(self):
        folder_dialog = QFileDialog(self)
        folder_paths = folder_dialog.getExistingDirectory(self, "Select Folder")
        print(folder_paths)

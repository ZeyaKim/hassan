import logging

from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


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

        group_box1 = QGroupBox("Group Box 1")

        # QVBoxLayout은 QGroupBox 내부에 위젯들을 수직으로 정렬합니다
        vbox_layout1 = QVBoxLayout()

        # QGroupBox에 위젯 추가
        vbox_layout1.addWidget(QPushButton("Button 1"))
        vbox_layout1.addWidget(QPushButton("Button 2"))

        group_box1.setLayout(vbox_layout1)

        group_box2 = QGroupBox("Group Box 2")

        vbox_layout2 = QVBoxLayout()
        vbox_layout2.addWidget(QPushButton("Button 3"))
        vbox_layout2.addWidget(QPushButton("Button 4"))

        group_box2.setLayout(vbox_layout2)

        layout = QHBoxLayout()
        layout.addWidget(group_box1)
        layout.addWidget(group_box2)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

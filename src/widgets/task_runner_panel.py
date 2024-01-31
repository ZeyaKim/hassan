from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class TaskRunnerPanel(QWidget):
    def __init__(self, logger, root_dir):
        super().__init__()

        self.logger = logger
        self.root_dir = root_dir

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        group_box = QGroupBox("Task Runner")
        layout.addWidget(group_box)

        group_box_layout = QVBoxLayout()

        progress_bar = QProgressBar()
        run_button = QPushButton("Run")

        h_layout = QHBoxLayout()
        h_layout.addWidget(progress_bar)
        h_layout.addWidget(run_button)

        group_box_layout.addLayout(h_layout)

        log_viewer_lable = QLabel("Progress Log")
        group_box_layout.addWidget(log_viewer_lable)

        log_viewer = QPlainTextEdit()
        group_box_layout.addWidget(log_viewer)

        group_box.setLayout(group_box_layout)

        layout.addWidget(group_box)

        self.setLayout(layout)

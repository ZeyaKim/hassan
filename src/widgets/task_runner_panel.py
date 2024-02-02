from PySide6.QtCore import QThread
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
    def __init__(self, logger, root_dir, task_runner):
        super().__init__()

        self.logger = logger
        self.root_dir = root_dir
        self.task_runner = task_runner

        self.init_ui()
        self.init_thread()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        group_box = QGroupBox("Task Runner")
        layout.addWidget(group_box)

        group_box_layout = QVBoxLayout()

        self.progress_bar = QProgressBar()
        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.run_tasks)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.progress_bar)
        h_layout.addWidget(self.run_button)

        group_box_layout.addLayout(h_layout)

        log_viewer_lable = QLabel("Progress Log")
        group_box_layout.addWidget(log_viewer_lable)

        log_viewer = QPlainTextEdit()
        log_viewer.setReadOnly(True)
        group_box_layout.addWidget(log_viewer)

        group_box.setLayout(group_box_layout)

        layout.addWidget(group_box)

        self.setLayout(layout)

    def init_thread(self):
        self.thread = QThread()
        self.task_runner.moveToThread(self.thread)

        self.thread.started.connect(self.task_runner.run)
        self.task_runner.finished.connect(self.on_tasks_finished)
        self.task_runner.finished.connect(self.thread.quit)
        self.task_runner.progress.connect(self.on_task_progress)

    def run_tasks(self):
        self.run_button.setEnabled(False)
        self.thread.start()

    def on_task_progress(self, value):
        self.progress_bar.setValue(value)

    def on_tasks_finished(self):
        self.run_button.setEnabled(True)
        self.progress_bar.setValue(0)

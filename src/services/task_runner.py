import os
import time

from PySide6.QtCore import QObject, Signal

from src.models.hassan_task import HassanTask
from src.utils.enums import ExtractableExtEnum


class TaskRunner(QObject):
    progress = Signal(int)
    finished = Signal()

    def __init__(
        self,
        logger,
        root_dir,
        audio_extractor,
        translator,
        subtitle_generator,
        path_viewer,
        config,
    ):
        super().__init__()  # QObject 초기화 추가
        self.logger = logger
        self.root_dir = root_dir
        self.audio_extractor = audio_extractor
        self.translator = translator
        self.subtitle_generator = subtitle_generator
        self.path_viewer = path_viewer
        self.config = config
        self.pending_tasks = []

        self.unique_tasks_paths = set()

    def run(self):
        task_settings = self.generate_execution_settings()
        paths = self.path_viewer.get_paths()
        for path, path_type in paths:
            if path_type == "Folder":
                self.add_folder_tasks(path, task_settings)
            else:
                self.enqueue_file_task(path, task_settings)

        for task in self.pending_tasks:
            task.execute()

        for i in range(100):
            self.progress.emit(i)
            time.sleep(0.1)

        self.on_finished()

        self.finished.emit()

    def generate_execution_settings(self):
        execute_settings = {
            "audio_extractor": {
                "whisper_model": self.config["audio_extractor"]["whisper_model"],
                "device": self.config["audio_extractor"]["device"],
            },
            "translator": {
                "deepl_api_key": self.config["translator"]["deepl_api_key"],
                "target_lang": self.config["translator"]["target_lang"],
            },
            "subtitle_generator": {
                "subtitle_ext": self.config["subtitle_generator"]["subtitle_ext"],
            },
        }

        return execute_settings

    def add_folder_tasks(self, folder_path: str, task_settings: dict):
        for path in os.listdir(folder_path):
            if os.path.isdir(os.path.join(folder_path, path)):
                self.add_folder_tasks(os.path.join(folder_path, path), task_settings)
            else:
                self.enqueue_file_task(os.path.join(folder_path, path), task_settings)
        pass

    def enqueue_file_task(self, file_path: str, task_settings: dict):
        if os.path.splitext(file_path)[1] not in [
            ext.value for ext in ExtractableExtEnum
        ]:
            return
        if file_path in self.unique_tasks_paths:
            return
        new_task = HassanTask(
            self.logger,
            self.root_dir,
            self.audio_extractor,
            self.translator,
            self.subtitle_generator,
            file_path,
            task_settings,
        )
        self.pending_tasks.append(new_task)
        self.unique_tasks_paths.add(file_path)

    def on_finished(self):
        self.path_viewer.on_finished()
        self.unique_tasks_paths.clear()
        self.pending_tasks.clear()

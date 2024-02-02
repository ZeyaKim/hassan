from PySide6.QtCore import QObject, QThread, Signal, Slot


class TaskRunner(QObject):
    progress = Signal(int)
    finished = Signal()

    def __init__(
        self, logger, root_dir, audio_extractor, translator, subtitle_generator
    ):
        super().__init__()  # QObject 초기화 추가
        self.logger = logger
        self.root_dir = root_dir
        self.audio_extractor = audio_extractor
        self.translator = translator
        self.subtitle_generator = subtitle_generator

    @Slot()
    def run(self):
        for i in range(100):
            self.progress.emit(i)
            QThread.msleep(100)
        self.finished.emit()

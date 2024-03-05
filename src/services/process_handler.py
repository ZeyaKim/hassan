import logging
import threading

from src.services.paths_storage import PathsStorage
from src.services.audio_extractor import AudioExtractor
from src.services.translator import Translator
from src.services.subtitle_generator import SubtitleGenerator

from PyQt5.QtCore import pyqtSignal, QObject


class ProcessHandler(QObject):
    finished = pyqtSignal()

    def __init__(
        self,
        paths_storage: PathsStorage,
        audio_extractor: AudioExtractor,
        translator: Translator,
        subtitle_generator: SubtitleGenerator,
    ):
        super().__init__()

        self.logger = logging.getLogger(__name__)
        self.paths_storage = paths_storage
        self.audio_extractor = audio_extractor
        self.translator = translator
        self.subtitle_generator = subtitle_generator

        self.is_running = False

    def run(self):
        try:
            if self.is_running:
                self.logger.warning("Process is already running")
                return

            if self.translator.deepl_api_key == "":
                self.logger.error("API key is not set")
                return

            self.is_running = True

            thread = threading.Thread(target=self._process_files)
            thread.start()
        except Exception as e:
            self.logger.error(f"Failed to run process: {e}")

    def _process_files(self):
        try:
            optimized_paths = self.paths_storage.optimize_paths()
            folders = optimized_paths["folder_paths"]
            files = optimized_paths["file_paths"]

            searched_files = self.paths_storage.recursive_search_files(folders)

            working_files = files + searched_files

            for file in working_files:
                self.process_audio_to_subtitle(file)
        finally:
            self.is_running = False
            self.finished.emit()

    def process_audio_to_subtitle(self, file):
        transcription = self.audio_extractor.extract_transcription(file)
        translated_transcription = self.translator.translate(transcription, file)
        self.subtitle_generator.create_subtitle(translated_transcription, file)

        self.logger.info(f"Processing {file} is done")

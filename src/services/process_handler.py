import logging
from src.services.paths_storage import PathsStorage
from src.services.audio_extractor import AudioExtractor
from src.services.translator import Translator
from src.services.subtitle_generator import SubtitleGenerator


class ProcessHandler:
    def __init__(
        self,
        paths_storage: PathsStorage,
        audio_extractor: AudioExtractor,
        translator: Translator,
        subtitle_generator: SubtitleGenerator,
    ):
        self.logger = logging.getLogger(__name__)
        self.paths_storage = paths_storage
        self.audio_extractor = audio_extractor
        self.translator = translator
        self.subtitle_generator = subtitle_generator

    def run(self):
        optimized_paths = self.paths_storage.optimize_paths()
        folders = optimized_paths["folder_paths"]
        files = optimized_paths["file_paths"]

        searched_files = self.paths_storage.recursive_search_files(folders)

        working_files = files + searched_files

        for file in working_files:
            self.process_audio_to_subtitle(file)

    def process_audio_to_subtitle(self, file):
        transcription = self.audio_extractor.extract_transcription(file)
        translated_transcription = self.translator.translate(transcription, file)
        self.subtitle_generator.create_subtitle(translated_transcription, file)

        self.logger.info(f"Processing {file} is done")

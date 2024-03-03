import pathlib
import logging


class PathsStorage:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.file_paths = []
        self.folder_paths = []

    def add_path(self, path):
        if not pathlib.Path(path).exists():
            self.logger.error(f"Path does not exist: {path}")
            return

        if pathlib.Path(path).is_file():
            self.add_file_path(path)
        elif pathlib.Path(path).is_dir():
            self.add_folder_path(path)

    def add_file_path(self, file_path):
        if file_path in self.file_paths:
            self.logger.warning(f"File already added: {file_path}")
            return

        if self.validate_supported_extension(file_path):
            self.file_paths.append(file_path)
            self.logger.info(f"Added file: {file_path}")

    def add_folder_path(self, folder_path):
        if folder_path in self.folder_paths:
            self.logger.warning(f"Folder already added: {folder_path}")
            return

        self.folder_paths.append(folder_path)
        self.logger.info(f"Added folder: {folder_path}")

    def validate_supported_extension(self, file_path):
        supported_extensions = [".mp3", ".wav", ".mp4"]
        if file_path.suffix in supported_extensions:
            return True
        return False

    def optimize_paths(self):
        sorted_folder_paths: list[pathlib.Path] = sorted(
            self.folder_paths, key=lambda x: str(x)
        )

        sub_folder_paths = []

        for idx, folder_path in enumerate(sorted_folder_paths):
            for sub_folder_path in sorted_folder_paths[idx + 1 :]:
                if sub_folder_path.is_relative_to(folder_path):
                    sub_folder_paths.append(sub_folder_path)
                else:
                    break

        optimized_folder_paths = [
            folder_path
            for folder_path in sorted_folder_paths
            if folder_path not in sub_folder_paths
        ]

        sub_file_paths = []

        for file_path in self.file_paths:
            for folder_path in optimized_folder_paths:
                if file_path.is_relative_to(folder_path):
                    sub_file_paths.append(file_path)
                    break

        optimized_file_paths = [
            file_path
            for file_path in self.file_paths
            if file_path not in sub_file_paths
        ]

        self.logger.info(
            f"Optimized folder paths: {optimized_folder_paths}\nOptimized file paths: {optimized_file_paths}"
        )

        return {
            "file_paths": optimized_file_paths,
            "folder_paths": optimized_folder_paths,
        }

    def recursive_search_files(self, folder_paths: list[pathlib.Path]):
        files = []
        for folder in folder_paths:
            for extension in [".mp3", ".wav", ".mp4"]:
                matched_files = folder.rglob(f"*{extension}")
                files.extend(matched_files)
        return files

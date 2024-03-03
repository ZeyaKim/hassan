import pathslib


class PathsStorage:
    def __init__(self):
        self.file_paths = []
        self.folder_paths = []

    def add_path(self, path):
        if not pathslib.Path(path).exists():
            return

        if pathslib.Path(path).is_file():
            self.add_file_path(path)
        elif pathslib.Path(path).is_dir():
            self.add_folder_path(path)

    def add_file_path(self, file_path):
        if self.validate_supported_extension(file_path):
            self.file_paths.append(file_path)

    def add_folder_path(self, folder_path):
        self.folder_paths.append(folder_path)

    def validate_supported_extension(self, file_path):
        supported_extensions = [".mp3", ".wav", ".mp4"]
        return pathslib.Path(file_path).suffix in supported_extensions

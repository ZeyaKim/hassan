class DuplicatePathError(Exception):
    pass


class NotSupportedExtensionError(Exception):
    pass


class AudioPathsManager:

    def __init__(self):
        self.file_paths = []
        self.folder_paths = []

    def _validate_file_extension(self, path):
        supported_extensions = [".mp3", ".wav", ".mp4"]
        if path.suffix in supported_extensions:
            return True
        else:
            return False

    def add_file_path(self, path):
        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist.")
        if not self._validate_file_extension(path):
            raise NotSupportedExtensionError(f"{path} is not supported.")
        if path in self.file_paths:
            raise DuplicatePathError(f"{path} is already added.")

        self.file_paths.append(path)

    def delete_file_path(self, path):
        if path not in self.file_paths:
            raise ValueError(f"{path} is not in the list.")
        self.file_paths.remove(path)

    def add_folder_path(self, path):
        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist.")
        if path in self.folder_paths:
            raise DuplicatePathError(f"{path} is already added.")

        self.folder_paths.append(path)

    def delete_folder_path(self, path):
        if path not in self.folder_paths:
            raise ValueError(f"{path} is not in the list.")
        self.folder_paths.remove(path)

    def get_paths(self):
        return {
            "file_paths": self.file_paths,
            "folder_paths": self.folder_paths,
        }

    def clear_paths(self):
        self.file_paths.clear()
        self.folder_paths.clear()

    def optimize_paths(self):
        optimized_folders = []
        optimized_files = []
        for folder in self.folder_paths:
            for parent in self.folder_paths:
                if folder.is_relative_to(parent) and parent != folder:
                    break
            else:
                optimized_folders.append(folder)

        for file in self.file_paths:
            for folder in optimized_folders:
                if file.is_relative_to(folder):
                    break
            else:
                optimized_files.append(file)

        return {
            "folder_paths": optimized_folders,
            "file_paths": optimized_files,
        }

    def recursive_search_paths(self, paths):
        optimized_folders = paths["folder_paths"]
        optimized_files = paths["file_paths"]

        supported_extensions = [".mp3", ".wav", ".mp4"]
        working_files_set = set()

        for folder in optimized_folders:
            for extension in supported_extensions:
                working_files_set.update(folder.rglob(f"*{extension}"))

        for file in optimized_files:
            working_files_set.add(file)

        return working_files_set

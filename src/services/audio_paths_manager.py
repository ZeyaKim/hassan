from src.utils.enums import SupportedAudioFormatEnum


class DuplicatePathError(Exception):
    pass


class NotSupportedExtensionError(Exception):
    pass


class AudioPathsManager:

    def __init__(self):
        self.file_paths = []
        self.folder_paths = []
        self.supported_audio_formats = {
            format.value for format in SupportedAudioFormatEnum
        }

    def _validate_file_extension(self, path):
        if path.suffix in self.supported_audio_formats:
            return True
        else:
            return False

    def add_path(self, path):
        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist.")

        if path.is_dir():
            paths_list = self.folder_paths

        elif path.is_file():
            if not self._validate_file_extension(path):
                raise NotSupportedExtensionError(f"{path} is not supported.")
            paths_list = self.file_paths

        if path in paths_list:
            raise DuplicatePathError(f"{path} is already added.")
        paths_list.append(path)

    def delete_path(self, path):
        if path.is_dir():
            paths_list = self.folder_paths
        elif path.is_file():
            paths_list = self.file_paths

        if path not in paths_list:
            raise ValueError(f"{path} is not in the list.")
        paths_list.remove(path)

    def get_paths(self):
        return {
            "file_paths": self.file_paths,
            "folder_paths": self.folder_paths,
        }

    def clear_paths(self):
        self.file_paths.clear()
        self.folder_paths.clear()

    def optimize_paths(self):

        sorted_folder_paths = sorted(self.folder_paths, key=lambda x: str(x))

        sub_folders = []
        for idx, folder in enumerate(sorted_folder_paths):
            if folder in sub_folders:
                break
            for sub_folder in sorted_folder_paths[idx + 1 :]:
                if sub_folder.is_relative_to(folder):
                    sub_folders.append(sub_folder)
                else:
                    break

        optimized_folders = [
            folder for folder in sorted_folder_paths if folder not in sub_folders
        ]

        optimized_files = [
            file
            for file in self.file_paths
            if not any(file.is_relative_to(folder) for folder in optimized_folders)
        ]

        return {
            "folder_paths": optimized_folders,
            "file_paths": optimized_files,
        }

    def recursive_search_paths(self, paths):
        optimized_folders = paths["folder_paths"]
        optimized_files = paths["file_paths"]

        working_files_set = set()

        for folder in optimized_folders:
            for extension in self.supported_audio_formats:
                working_files_set.update(folder.rglob(f"*{extension}"))

        for file in optimized_files:
            working_files_set.add(file)

        return working_files_set

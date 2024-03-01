"""
# AudioPathsManager 클래스 요구사항

## 1. 파일 확장자 검증 함수
- **목표**: 입력받은 파일 경로의 확장자가 Whisper에서 지원하는 확장자인지 확인한다.
- **요구사항**:
    1. 입력받은 파일 경로의 확장자가 지원하는 확장자인지 확인한다.
    2. 지원하는 확장자인 경우 True를 반환한다.
    3. 지원하는 확장자가 아닌 경우 False를 반환한다.

## 2. 파일 경로 입력 함수1
- **목표**: 파일 경로를 입력받아 클래스의 self.file_paths에 저장한다.
- **요구사항**: 
    1. 클래스의 self.file_paths에 파일 경로가 제대로 입력되었는지 확인
    2. 파일 경로가 존재하지 않는 경우, `FileNotFoundError`가 발생한다.
    3. 중복된 파일 경로가 입력된 경우, `DuplicatePathError`가 발생
    
## 3. 파일 경로 삭제 함수
- **목표**: 파일 경로를 입력받아 클래스의 self.file_paths에서 삭제한다.
- **요구사항**: 
    1. 클래스의 self.file_paths에서 파일 경로가 제대로 삭제되었는지 확인
    2. 파일 경로가 존재하지 않는 경우, `ValueError`가 발생한다.
    
## 4. 폴더 경로 입력 함수
- **목표**: 폴더 경로를 입력받아 클래스의 self.folder_paths에 저장한다.
- **요구사항**: 
    1. 클래스의 self.folder_paths에 폴더 경로가 제대로 입력되었는지 확인
    2. 폴더 경로가 존재하지 않는 경우, FileNotFoundError가 발생한다.
    3. 중복된 폴더 경로가 입력된 경우, `DuplicatePathError`가 발생
    
## 5. 폴더 경로 삭제 함수
- **목표**: 폴더 경로를 입력받아 클래스의 self.folder_paths에서 삭제한다.
- **요구사항**: 
    1. 클래스의 self.folder_paths에서 폴더 경로가 제대로 삭제되었는지 확인
    2. 폴더 경로가 존재하지 않는 경우, `ValueError`가 발생한다.
    
## 6. 저장된 경로 반환 함수
- **목표**: 저장된 파일 및 폴더 경로를 반환한다.
- **요구사항**: 
    1. 저장된 파일 경로와 폴더 경로를 각각 list 형태로 반환한다.
    2. 저장된 경로가 없는 경우, 빈 리스트를 반환한다.

## 7. 파일 및 폴더 경로 초기화 함수
- **목표**: 저장된 파일 및 폴더 경로를 초기화한다.
- **요구사항**: 
    1. 저장된 파일 및 폴더 경로를 초기화한다.
    2. 초기화 후, 저장된 경로가 없는지 확인한다.

## 8. 경로 중복 최적화 함수
-- **목표**: 저장된 폴더 내에 있는 다른 저장된 폴더나 파일들을 삭제한 후 별도의 리스트로 반환한다.
-- **요구사항**: 
    1. 저장된 폴더 내에 있는 다른 저장된 폴더를 삭제한다.
    2. 저장된 폴더 내에 있는 다른 저장된 파일을 삭제한다.
    3. 삭제 후, 저장된 폴더와 파일 경로를 각각 list 형태로 반환한다.
    
## 9. 폴더 재귀 탐색 함수
-- **목표**: 저장된 폴더 내에 있는 모든 파일을 재귀적으로 탐색하여 리스트로 반환한다.
-- **요구사항**: 
    1. 저장된 폴더 내에 있는 모든 파일을 재귀적으로 탐색하여 리스트로 반환한다.
    2. 요구하는 확장자의 파일만 리스트에 포함시킨다.
"""

import unittest
import tempfile
import pathlib

from src.services.audio_paths_manager import (
    AudioPathsManager,
    DuplicatePathError,
    NotSupportedExtensionError,
)


class TestAudioPathsManager(unittest.TestCase):
    def setUp(self):
        # 임시 디렉토리 생성
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = pathlib.Path(self.temp_dir.name)

        # 올바른 오디오 파일 생성
        self.correct_audio_path = self.test_dir / "test_audio.mp3"
        self.correct_audio_path.touch()

        # 잘못된 확장자를 가진 오디오 파일 생성
        self.non_supported_extension_audio_path = self.test_dir / "test_audio.jpg"
        self.non_supported_extension_audio_path.touch()

        # 존재하지 않는 오디오 파일 경로 설정
        self.wrong_audio_path = self.test_dir / "not_exist.mp3"

        # 올바른 폴더 경로 생성
        self.correct_folder_path = self.test_dir / "test_folder"
        self.correct_folder_path.mkdir()

        # 잘못된 폴더 경로 생성
        self.wrong_folder_path = self.test_dir / "not_exist_folder"

        self.audio_paths_manager = AudioPathsManager()

    def test_validate_supported_file_extension(self):
        """지원하는 확장자의 파일 확장자 검증 테스트"""

        self.assertTrue(
            self.audio_paths_manager._validate_file_extension(self.correct_audio_path)
        )

    def test_validate_non_supported_file_extension(self):
        """지원하지 않는 확장자의 파일 확장자 검증 테스트"""

        self.assertFalse(
            self.audio_paths_manager._validate_file_extension(
                self.non_supported_extension_audio_path
            )
        )

    def test_add_file_path_success(self):
        """파일 경로 입력 성공 테스트"""

        self.audio_paths_manager.add_path(self.correct_audio_path)
        self.assertIn(self.correct_audio_path, self.audio_paths_manager.file_paths)

    def test_add_file_path_fail(self):
        """잘못된 파일 경로 입력 실패 테스트"""

        with self.assertRaises(FileNotFoundError):
            self.audio_paths_manager.add_path(self.wrong_audio_path)

    def test_add_file_path_duplicate(self):
        """중복된 파일 경로 입력 실패 테스트"""

        self.audio_paths_manager.add_path(self.correct_audio_path)
        with self.assertRaises(DuplicatePathError):
            self.audio_paths_manager.add_path(self.correct_audio_path)

    def test_add_file_path_not_supported_extension(self):
        """지원하지 않는 확장자의 파일 경로 입력 실패 테스트"""

        with self.assertRaises(NotSupportedExtensionError):
            self.audio_paths_manager.add_path(self.non_supported_extension_audio_path)

    def test_delete_file_path_success(self):
        """파일 경로 삭제 성공 테스트"""

        self.audio_paths_manager.file_paths = [self.correct_audio_path]
        self.audio_paths_manager.delete_path(self.correct_audio_path)
        self.assertNotIn(self.correct_audio_path, self.audio_paths_manager.file_paths)

    def test_delete_non_exist_file_path(self):
        """잘못된 파일 경로 삭제 실패 테스트"""

        with self.assertRaises(ValueError):
            self.audio_paths_manager.delete_path(self.correct_audio_path)

    def test_add_folder_path_success(self):
        """폴더 경로 입력 성공 테스트"""

        self.audio_paths_manager.add_path(self.correct_folder_path)
        self.assertIn(self.correct_folder_path, self.audio_paths_manager.folder_paths)

    def test_add_folder_path_fail(self):
        """잘못된 폴더 경로 입력 실패 테스트"""

        with self.assertRaises(FileNotFoundError):
            self.audio_paths_manager.add_path(self.wrong_folder_path)

    def test_add_folder_path_duplicate(self):
        """중복된 폴더 경로 입력 실패 테스트"""

        self.audio_paths_manager.add_path(self.correct_folder_path)
        with self.assertRaises(DuplicatePathError):
            self.audio_paths_manager.add_path(self.correct_folder_path)

    def test_delete_folder_path_success(self):
        """폴더 경로 삭제 성공 테스트"""

        self.audio_paths_manager.folder_paths = [self.correct_folder_path]
        self.audio_paths_manager.delete_path(self.correct_folder_path)
        self.assertNotIn(
            self.correct_folder_path, self.audio_paths_manager.folder_paths
        )

    def test_delete_non_exist_folder_path(self):
        """잘못된 폴더 경로 삭제 실패 테스트"""

        with self.assertRaises(ValueError):
            self.audio_paths_manager.delete_path(self.correct_folder_path)

    def test_get_paths_success(self):
        """저장된 경로 반환 성공 테스트"""

        self.audio_paths_manager.add_path(self.correct_audio_path)
        self.audio_paths_manager.add_path(self.correct_folder_path)

        self.assertEqual(
            self.audio_paths_manager.get_paths(),
            {
                "folder_paths": [self.correct_folder_path],
                "file_paths": [self.correct_audio_path],
            },
        )

    def test_get_paths_blank(self):
        """저장된 경로가 없는 경우 반환 테스트"""

        self.assertEqual(
            self.audio_paths_manager.get_paths(),
            {"folder_paths": [], "file_paths": []},
        )

    def test_clear_paths(self):
        """저장된 경로 초기화 테스트"""

        self.audio_paths_manager.add_path(self.correct_audio_path)
        self.audio_paths_manager.add_path(self.correct_folder_path)

        self.assertEqual(
            self.audio_paths_manager.get_paths(),
            {
                "folder_paths": [self.correct_folder_path],
                "file_paths": [self.correct_audio_path],
            },
        )

        self.audio_paths_manager.clear_paths()
        self.assertEqual(
            self.audio_paths_manager.get_paths(),
            {"folder_paths": [], "file_paths": []},
        )

    def test_optimize_paths(self):
        """경로 중복 최적화 테스트"""

        sub_folder = self.correct_folder_path / "sub_folder"
        sub_folder.mkdir()
        sub_audio = self.correct_folder_path / "sub_folder" / "test.mp3"
        sub_audio.touch()

        self.audio_paths_manager.add_path(self.correct_audio_path)
        self.audio_paths_manager.add_path(self.correct_folder_path)
        self.audio_paths_manager.add_path(sub_folder)
        self.audio_paths_manager.add_path(sub_audio)

        self.assertEqual(
            self.audio_paths_manager.optimize_paths(),
            {
                "folder_paths": [self.correct_folder_path],
                "file_paths": [self.correct_audio_path],
            },
        )

    def test_recursive_search_paths(self):
        """폴더 재귀 탐색 테스트"""

        recursive_audio_dir = self.test_dir / "test_folder" / "sub_folder"
        recursive_audio_dir.mkdir(parents=True)

        (recursive_audio_dir / "test_1.mp3").touch()
        (recursive_audio_dir / "test_2.mp3").touch()

        optimized_paths = {
            "folder_paths": [recursive_audio_dir],
            "file_paths": [self.correct_audio_path],
        }

        self.assertEqual(
            self.audio_paths_manager.recursive_search_paths(paths=optimized_paths),
            {
                self.correct_audio_path,
                recursive_audio_dir / "test_1.mp3",
                recursive_audio_dir / "test_2.mp3",
            },
        )

    def tearDown(self):
        # 임시 디렉토리 정리
        self.temp_dir.cleanup()


if __name__ == "__main__":
    unittest.main()

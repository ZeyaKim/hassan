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

import pytest

from src.services.audio_paths_manager import (
    AudioPathsManager,
    DuplicatePathError,
    NotSupportedExtensionError,
)


@pytest.fixture
def audio_paths_manager():
    """AudioPathsManager 객체 반환"""
    audio_paths_manager = AudioPathsManager()
    yield audio_paths_manager


@pytest.fixture
def correct_audio_path(tmp_path):
    """올바른 오디오 파일 경로 반환"""
    correct_audio_path = tmp_path / "test_audio.mp3"
    correct_audio_path.touch()
    yield correct_audio_path


@pytest.fixture
def wrong_extension_audio_path(tmp_path):
    """잘못된 확장자의 오디오 파일 경로 반환"""
    wrong_extension_audio_path = tmp_path / "test_audio.jpg"
    wrong_extension_audio_path.touch()
    yield wrong_extension_audio_path


@pytest.fixture
def wrong_audio_path(tmp_path):
    """잘못된 오디오 파일 경로 반환"""
    wrong_audio_path = tmp_path / "not_exist.mp3"
    yield wrong_audio_path


@pytest.fixture
def correct_folder_path(tmp_path):
    """올바른 폴더 경로 반환"""
    correct_folder_path = tmp_path / "test_folder"
    correct_folder_path.mkdir()
    yield correct_folder_path


@pytest.fixture
def wrong_folder_path(tmp_path):
    """잘못된 폴더 경로 반환"""
    wrong_folder_path = tmp_path / "not_exist"
    yield wrong_folder_path


def test_validate_correct_file_extension(audio_paths_manager, correct_audio_path):
    """파일 확장자 검증 테스트"""

    assert audio_paths_manager._validate_file_extension(correct_audio_path) is True


def test_validate_wrong_file_extension(audio_paths_manager, wrong_extension_audio_path):
    """잘못된 확장자의 파일 확장자 검증 테스트"""

    assert (
        audio_paths_manager._validate_file_extension(wrong_extension_audio_path)
        is False
    )


def test_add_file_path_success(audio_paths_manager, correct_audio_path):
    """파일 경로 입력 성공 테스트"""

    audio_paths_manager.add_path(correct_audio_path)
    assert correct_audio_path in audio_paths_manager.file_paths


def test_add_file_path_fail(audio_paths_manager, wrong_audio_path):
    """잘못된 파일 경로 입력 실패 테스트"""

    with pytest.raises(FileNotFoundError):
        audio_paths_manager.add_path(wrong_audio_path)


def test_add_file_path_duplicate(audio_paths_manager, correct_audio_path):
    """중복된 파일 경로 입력 실패 테스트"""

    audio_paths_manager.add_path(correct_audio_path)
    with pytest.raises(DuplicatePathError):
        audio_paths_manager.add_path(correct_audio_path)


def test_add_file_path_not_supported_extension(
    audio_paths_manager, wrong_extension_audio_path
):
    """지원하지 않는 확장자의 파일 경로 입력 실패 테스트"""

    with pytest.raises(NotSupportedExtensionError):
        audio_paths_manager.add_path(wrong_extension_audio_path)


def test_delete_file_path_success(audio_paths_manager, correct_audio_path):
    """파일 경로 삭제 성공 테스트"""

    audio_paths_manager.file_paths = [correct_audio_path]
    audio_paths_manager.delete_path(correct_audio_path)
    assert correct_audio_path not in audio_paths_manager.file_paths


def test_delete_file_path_fail(audio_paths_manager, correct_audio_path):
    """잘못된 파일 경로 삭제 실패 테스트"""

    with pytest.raises(ValueError):
        audio_paths_manager.delete_path(correct_audio_path)


def test_add_folder_path_success(audio_paths_manager, correct_folder_path):
    """폴더 경로 입력 성공 테스트"""

    audio_paths_manager.add_path(correct_folder_path)
    assert correct_folder_path in audio_paths_manager.folder_paths


def test_add_folder_path_fail(audio_paths_manager, wrong_folder_path):
    """잘못된 폴더 경로 입력 실패 테스트"""

    with pytest.raises(FileNotFoundError):
        audio_paths_manager.add_path(wrong_folder_path)


def test_add_folder_path_duplicate(audio_paths_manager, correct_folder_path):
    """중복된 폴더 경로 입력 실패 테스트"""

    audio_paths_manager.add_path(correct_folder_path)
    with pytest.raises(DuplicatePathError):
        audio_paths_manager.add_path(correct_folder_path)


def test_delete_folder_path_success(audio_paths_manager, correct_folder_path):
    """폴더 경로 삭제 성공 테스트"""

    audio_paths_manager.folder_paths = [correct_folder_path]
    audio_paths_manager.delete_path(correct_folder_path)
    assert correct_folder_path not in audio_paths_manager.folder_paths


def test_delete_folder_path_fail(audio_paths_manager, tmp_path):
    """잘못된 폴더 경로 삭제 실패 테스트"""

    with pytest.raises(ValueError):
        audio_paths_manager.delete_path(tmp_path)


def test_get_paths_success(
    audio_paths_manager, correct_audio_path, correct_folder_path
):
    """저장된 경로 반환 성공 테스트"""

    audio_paths_manager.add_path(correct_audio_path)
    audio_paths_manager.add_path(correct_folder_path)

    assert audio_paths_manager.get_paths() == {
        "folder_paths": [correct_folder_path],
        "file_paths": [correct_audio_path],
    }


def test_get_paths_blank(audio_paths_manager):
    """저장된 경로가 없는 경우 반환 테스트"""

    assert audio_paths_manager.get_paths() == {"folder_paths": [], "file_paths": []}


def test_clear_paths(audio_paths_manager, correct_audio_path, correct_folder_path):
    """저장된 경로 초기화 테스트"""

    audio_paths_manager.add_path(correct_audio_path)
    audio_paths_manager.add_path(correct_folder_path)

    audio_paths_manager.clear_paths()
    assert audio_paths_manager.get_paths() == {"folder_paths": [], "file_paths": []}


def test_optimize_paths(audio_paths_manager, correct_audio_path, correct_folder_path):
    """경로 중복 최적화 테스트"""

    audio_paths_manager.add_path(correct_audio_path)
    audio_paths_manager.add_path(correct_folder_path)

    sub_folder = correct_folder_path / "sub_folder"
    sub_folder.mkdir()
    sub_audio = correct_folder_path / "sub_folder" / "test.mp3"
    sub_audio.touch()

    audio_paths_manager.add_path(sub_folder)
    audio_paths_manager.add_path(sub_audio)

    assert audio_paths_manager.optimize_paths() == {
        "folder_paths": [correct_folder_path],
        "file_paths": [correct_audio_path],
    }


def test_recursive_search_paths(audio_paths_manager, correct_audio_path, tmp_path):
    """폴더 재귀 탐색 테스트"""

    recursive_audio_dir = tmp_path / "test_folder" / "sub_folder"
    recursive_audio_dir.mkdir(parents=True)

    (recursive_audio_dir / "test_1.mp3").touch()
    (recursive_audio_dir / "test_2.mp3").touch()

    optimized_paths = {
        "folder_paths": [recursive_audio_dir],
        "file_paths": [correct_audio_path],
    }

    assert audio_paths_manager.recursive_search_paths(paths=optimized_paths) == {
        correct_audio_path,
        recursive_audio_dir / "test_1.mp3",
        recursive_audio_dir / "test_2.mp3",
    }

"""
# AudioExtractor 클래스 테스트 요구사항

## 1. 위스퍼 모델 로드 테스트
- **목표**: load_model 메서드를 호출하여 위스퍼 모델을 로드한다.
- **요구사항**:
    1. load_model 메서드를 호출하여 위스퍼 모델을 로드한다.
    2. 로드된 모델은 `openai-whisper.Whisper` 클래스의 인스턴스여야 한다.
    3. 클래스 생성 시 설정된 `model`과 `device` 설정이 모델 로드 시에도 적용되어야 한다.

## 2. 오디오 파일 텍스트 변환 테스트
- **목표**: 주어진 경로의 오디오 파일을 `{start_time: float, end_time: float, text: str}` 형식을 갖는 리스트로 변환하여 반환한다.
- **요구사항**:
    1. 메서드는 주어진 경로의 오디오 파일을 읽고, `{start_time: float, end_time: float, text: str}` 형식의 항목을 갖는 리스트로 추출한다.
    2. 추출된 각 문장 데이터는 정확한 시간 정보(start_time, end_time)와 텍스트 정보(text)를 포함해야 한다.
    3. 정상적인 입력에 대해 변환된 리스트는 비어 있지 않아야 하며, 모든 항목은 정해진 형식을 준수해야 한다.

## 3. 오디오 파일 텍스트 변환 실패 테스트
- **목표**: 잘못된 경로의 오디오 파일을 전달받았을 때, `FileNotFoundError`가 발생한다.
- **요구사항**:
    1. 존재하지 않는 파일 경로를 메서드에 전달하면, `FileNotFoundError` 예외가 발생해야 한다.

## 4. 텍스트 파일 저장 테스트
- **목표**: 변환된 트랜스크립션 리스트를 `'start_time~end_time\ntext\n\n'` 형식으로 텍스트 파일에 저장한다.
- **요구사항**:
    1. 변환된 트랜스크립션 리스트는 주어진 형식('`{start_time}~{end_time}\n{text}\n\n`')에 따라 텍스트 파일에 저장되어야 한다.
    2. 저장된 텍스트 파일은 각 트랜스크립션 항목 사이에 한 줄의 공백을 포함해야 한다.
    3. 파일 저장 후, 저장된 내용을 검증하여 변환된 데이터가 정확하게 파일에 기록되었는지 확인한다.
"""

import pytest
import pathlib
import shutil

import whisper

from src.services.audio_extractor import AudioExtractor


@pytest.fixture
def test_audio_path(tmp_path):
    """테스트 패스 반환"""
    original_audio_path = (
        pathlib.Path("tests") / "test_assets" / "test_audio.mp3"
    )  # 테스트용 오디오 파일 경로

    tmp_audio_path = tmp_path / original_audio_path.name  # 임시 오디오 파일 경로
    shutil.copy(original_audio_path, tmp_audio_path)  # 오디오 파일 복사

    yield tmp_audio_path


@pytest.fixture
def audio_extractor():
    """AudioExtractor 객체 반환"""
    audio_extractor = AudioExtractor()
    yield audio_extractor


def test_load_model_success(audio_extractor):
    """위스퍼 모델 로드 테스트"""
    result = audio_extractor.load_model()  # 모델 로드
    assert isinstance(
        result, whisper.Whisper
    )  # 모델이 Whisper 클래스의 인스턴스인지 확인


def test_transcribe_audio_success(audio_extractor, test_audio_path):
    """오디오 파일을 텍스트로 변환하는 테스트"""
    result = audio_extractor.transcribe_audio(test_audio_path)
    assert isinstance(result, list)  # 결과가 리스트인지 확인
    assert len(result) != 0  # 결과가 비어있지 않은지 확인

    for sentence in result:  # 결과의 각 문장에 대해 확인
        assert all(
            isinstance(sentence[key], float)
            for key in [
                "start",
                "end",
            ]  # start_time, end_time이 float인지 확인
        )
        assert isinstance(sentence["text"], str)  # text가 str인지 확인

    transcription_path = (
        test_audio_path.parent
        / f"{test_audio_path.stem}_transcription.txt"  # 텍스트 파일 경로
    )
    assert transcription_path.exists()  # 텍스트 파일이 존재하는지 확인


def test_transcribe_audio_wrong_path(audio_extractor):
    """잘못된 경로의 오디오 파일을 변환하는 테스트"""
    wrong_path = pathlib.Path("test_assets") / "wrong_audio.mp3"
    with pytest.raises(FileNotFoundError):  # FileNotFoundError가 발생하는지 확인
        audio_extractor.transcribe_audio(wrong_path)


def test_save_transcription_success(audio_extractor, test_audio_path):
    """텍스트 파일 저장 테스트"""
    transcription_path = (
        test_audio_path.parent
        / f"{test_audio_path.stem}_transcription.txt"  # 텍스트 파일 경로
    )
    transcription = [
        {"start": 0.0, "end": 1.5, "text": "This is the first sentence."},
        {"start": 2.0, "end": 3.5, "text": "This is the second sentence."},
    ]  # 텍스트 파일에 저장할 텍스트
    audio_extractor.save_transcription(transcription, transcription_path)

    with pathlib.Path(transcription_path).open("r") as file:
        transcription_content = file.readlines()  # 텍스트 파일 내용을 읽어옴
        assert len(transcription_content) == len(transcription) * 3

        for i in range(len(transcription)):
            assert (
                transcription_content[i * 3]
                == f"{transcription[i]['start']:.2f} ~ {transcription[i]['end']:.2f}\n"
            )
            assert transcription_content[i * 3 + 1] == f"{transcription[i]['text']}\n"
            assert transcription_content[i * 3 + 2] == "\n"

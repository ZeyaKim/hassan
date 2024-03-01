"""
# AudioExtractor 클래스 테스트 요구사항

## 1. 오디오 파일 텍스트 변환 테스트
- **목표**: 주어진 경로의 오디오 파일을 `{start_time: float, end_time: float, text: str}` 형식을 갖는 리스트로 변환하여 반환한다.
- **요구사항**:
    1. 메서드는 주어진 경로의 오디오 파일을 읽고, `{start_time: float, end_time: float, text: str}` 형식의 항목을 갖는 리스트로 추출한다.
    2. 추출된 각 문장 데이터는 정확한 시간 정보(start_time, end_time)와 텍스트 정보(text)를 포함해야 한다.
    3. 정상적인 입력에 대해 변환된 리스트는 비어 있지 않아야 하며, 모든 항목은 정해진 형식을 준수해야 한다.

## 2. 오디오 파일 텍스트 변환 실패 테스트
- **목표**: 잘못된 경로의 오디오 파일을 전달받았을 때, `FileNotFoundError`가 발생한다.
- **요구사항**:
    1. 존재하지 않는 파일 경로를 메서드에 전달하면, `FileNotFoundError` 예외가 발생해야 한다.

## 3. 텍스트 파일 저장 테스트
- **목표**: 변환된 트랜스크립션 리스트를 `'start_time~end_time\ntext\n\n'` 형식으로 텍스트 파일에 저장한다.
- **요구사항**:
    1. 변환된 트랜스크립션 리스트는 주어진 형식('`{start_time}~{end_time}\n{text}\n\n`')에 따라 텍스트 파일에 저장되어야 한다.
    2. 저장된 텍스트 파일은 각 트랜스크립션 항목 사이에 한 줄의 공백을 포함해야 한다.
    3. 파일 저장 후, 저장된 내용을 검증하여 변환된 데이터가 정확하게 파일에 기록되었는지 확인한다.
"""

import pathlib
import shutil
import unittest
import tempfile

from src.services.audio_extractor import AudioExtractor


class TestAudioExtractor(unittest.TestCase):
    """AudioExtractor 클래스 테스트"""

    def setUp(self):
        """테스트 환경 설정"""

        self.test_audio_path = (
            pathlib.Path("tests") / "test_assets" / "test_audio.mp3"
        )  # 테스트용 오디오 파일 경로

        self.tmp_dir = tempfile.TemporaryDirectory()
        self.test_dir = pathlib.Path(self.tmp_dir.name)
        self.tmp_audio_path = (
            self.test_dir / self.test_audio_path.name
        )  # 임시 오디오 파일 경로
        shutil.copy(self.test_audio_path, self.tmp_audio_path)

        self.audio_extractor = AudioExtractor()

    def test_transcribe_audio_success(self):
        """오디오 파일을 텍스트로 변환하는 테스트"""

        self.audio_extractor.load_model()
        result = self.audio_extractor.transcribe_audio(self.tmp_audio_path)
        self.assertIsInstance(result, list)
        self.assertNotEqual(len(result), 0)

        for sentence in result:
            self.assertIsInstance(sentence["start"], float)
            self.assertIsInstance(sentence["end"], float)
            self.assertIsInstance(sentence["text"], str)

    def test_extract_audio_wrong_path(self):
        """잘못된 경로의 오디오 파일을 변환하는 테스트"""

        wrong_path = pathlib.Path("test_assets") / "wrong_audio.mp3"
        with self.assertRaises(FileNotFoundError):
            self.audio_extractor.extract_audio(wrong_path)

    def test_save_transcription_success(self):
        """텍스트 파일 저장 테스트"""

        transcription_path = (
            self.test_dir / f"{self.tmp_audio_path.stem}_transcription.txt"
        )
        transcription = [
            {"start": 0.0, "end": 1.5, "text": "This is the first sentence."},
            {"start": 2.0, "end": 3.5, "text": "This is the second sentence."},
        ]

        self.audio_extractor.save_transcription(transcription, transcription_path)

        with transcription_path.open("r") as file:
            transcription_content = file.readlines()
            self.assertEqual(len(transcription_content), len(transcription) * 3)

            for i in range(len(transcription)):
                self.assertEqual(
                    transcription_content[i * 3],
                    f"{transcription[i]['start']:.2f} ~ {transcription[i]['end']:.2f}\n",
                )

    def tearDown(self):
        """테스트 환경 정리"""
        self.tmp_dir.cleanup()  # 임시 디렉토리 삭제

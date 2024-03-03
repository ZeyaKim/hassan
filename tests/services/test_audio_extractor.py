"""
# AudioExtractor 클래스 테스트 요구사항

1. 오디오 텍스트 추출 함수
- **목표**: 오디오 파일에서 텍스트를 추출한 후 반환한다.
- **요구사항**:
    1. 입력받은 오디오 파일이 존재하는지 확인하고, 존재하지 않는 경우 `FileNotFoundError`가 발생한다.
    2. 모델이 로드되어 있지 않은 경우, 모델을 로드한다.
    3. 오디오 파일을 텍스트로 변환한 후, 변환된 텍스트 리스트를 저장한 후 반환한다.
    4. 변환된 텍스트 리스트의 각 항목은 {'start': ~, 'end': ~, 'text': ~} 형태이다.
    5. 변환된 텍스트 리스트의 각 항목의 start, end는 float 형태이고, text는 str 형태이다.
    
2. 모델 로드 함수
- **목표**: 모델을 로드하고 오디오 파일을 로드한다.
- **요구사항**:
    1. 주어진 세팅을 적용하여 모델을 로드한다.
    2. 주어진 오디오 파일을 로드한다.

3. 오디오 파일 변환 함수
- **목표**: 오디오 파일을 텍스트로 변환한 후 결과 맵에서 필요한 정보를 추출한 후 반환한다.
- **요구사항**:
    1. 로드된 오디오 파일을 모델을 사용해 변환한다.
    2. 변환된 텍스트 리스트에서 필요한 정보를 추출한 후 반환한다.
    3. 변환된 텍스트 리스트가 비어있는 경우, 빈 리스트를 반환한다.
    
4. 텍스트 파일 저장 함수
- **목표**: 변환된 텍스트 리스트를 파일로 저장한다.
- **요구사항**:
    1. 변환된 텍스트 리스트를 파일로 저장한다.
    2. 저장되는 텍스트의 형식은 f"{start:.2f} ~ {end:.2f}\n{text}\n\n"이다.
    3. 저장된 파일에 변환된 텍스트 리스트가 제대로 저장되었는지 확인한다.
"""

import unittest
from unittest.mock import patch, MagicMock
from src.services.audio_extractor import AudioExtractor
import whisper


class TestAudioExtractor(unittest.TestCase):
    def setUp(self):
        self.audio_extractor = AudioExtractor()

    @patch("whisper.load_model")
    def test_load_model(self, mock_load_model):
        """모델을 로드하는 함수를 테스트합니다."""

        mock_whisper_instance = MagicMock(spec=whisper.Whisper)
        mock_load_model.return_value = mock_whisper_instance

        self.audio_extractor.load_model()
        self.assertIsInstance(self.audio_extractor.model, whisper.Whisper)
        mock_load_model.assert_called_with(name="small", device="cpu")

    @patch("src.services.audio_extractor.whisper.load_model")
    @patch("src.services.audio_extractor.whisper.load_audio")
    def test_transcribe_audio(self, mock_load_audio, mock_load_model):
        """오디오 파일을 텍스트로 변환하는 함수를 테스트합니다."""
        mock_whisper_instance = MagicMock(spec=whisper.Whisper)
        mock_load_model.return_value = mock_whisper_instance
        mock_whisper_instance.transcribe.return_value = {
            "segments": [
                {"start": 0.0, "end": 1.0, "text": "This is First Sentence."},
                {"start": 1.5, "end": 2.5, "text": "This is Second Sentence."},
            ]
        }

        # 모델을 먼저 로드합니다.
        self.audio_extractor.load_model()

        transcription_list = self.audio_extractor.transcribe_audio("fake_audio.mp3")
        expected_transcription = [
            {"start": 0.0, "end": 1.0, "text": "This is First Sentence."},
            {"start": 1.5, "end": 2.5, "text": "This is Second Sentence."},
        ]
        self.assertEqual(transcription_list, expected_transcription)
        mock_load_audio.assert_called_once_with("fake_audio.mp3")
        mock_whisper_instance.transcribe.assert_called_once()

    @patch("pathlib.Path.exists")
    @patch("src.services.audio_extractor.AudioExtractor.transcribe_audio")
    @patch("src.services.audio_extractor.AudioExtractor.save_transcription")
    @patch("src.services.audio_extractor.AudioExtractor.load_model")
    def test_extract_audio(
        self,
        mock_load_model,
        mock_save_transcription,
        mock_transcribe_audio,
        mock_exists,
    ):
        """오디오 파일에서 텍스트를 추출하는 함수를 테스트합니다."""

        # 모킹된 함수들이 반환할 값 설정
        mock_exists.return_value = True
        mock_transcribe_audio.return_value = [
            {"start": 0.0, "end": 1.0, "text": "This is a test."}
        ]

        # 테스트 대상 메소드 호출
        transcription_list = self.audio_extractor.extract_audio("fake_audio.mp3")

        # 반환된 트랜스크립션이 예상된 값과 일치하는지 검사
        expected_transcription = [{"start": 0.0, "end": 1.0, "text": "This is a test."}]
        self.assertEqual(transcription_list, expected_transcription)

        # 모킹된 함수들이 적절히 호출되었는지 검사
        mock_exists.assert_called_once_with()
        mock_load_model.assert_called_once()
        mock_transcribe_audio.assert_called_once_with("fake_audio.mp3")
        mock_save_transcription.assert_called_once()

    def test_save_transcription(self):
        """변환된 텍스트 리스트를 파일로 저장하는 함수를 테스트합니다."""

        # 테스트 대상 메소드 호출
        transcription = [
            {"start": 0.0, "end": 1.0, "text": "This is a test."},
            {"start": 1.5, "end": 2.5, "text": "This is another test."},
        ]
        transcription_path = "fake_audio_transcription.txt"
        self.audio_extractor.save_transcription(transcription, transcription_path)

        # 저장된 파일을 읽어서 반환된 텍스트 리스트와 일치하는지 검사
        with open(transcription_path, "r", encoding="utf-8") as file:
            saved_transcription = file.read()

            self.assertEqual(
                saved_transcription,
                "0.00 ~ 1.00\nThis is a test.\n\n1.50 ~ 2.50\nThis is another test.\n\n",
            )


# 유닛 테스트 실행
if __name__ == "__main__":
    unittest.main()

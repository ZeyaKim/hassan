import logging
import torch
import whisper


class AudioExtractor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setting = {
            "model": "medium",
            "device": "cuda" if torch.cuda.is_available() else "cpu",
        }
        self.model = None

    def extract_transcription(self, file_path):
        if self.model is None:
            self.model = whisper.load_model(
                device=self.setting["device"], name=self.setting["model"]
            )

        working_audio = whisper.load_audio(str(file_path))

        segments = self.model.transcribe(working_audio, fp16=False)["segments"]

        transcription = [
            {
                "start": segment["start"],
                "end": segment["end"],
                "text": str(segment["text"]),
            }
            for segment in segments
        ]

        self.logger.info(f"Transcription of {file_path} is done")
        return transcription

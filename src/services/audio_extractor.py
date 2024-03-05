import logging
import whisper
import torch


class AudioExtractor:
    def __init__(self):
        print(torch.__version__)
        self.logger = logging.getLogger(__name__)
        try:
            self.setting = {"model": "medium", "device": "cuda"}
        except Exception:
            self.logger.error("Cuda is not available")

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

        self.save_transcription(transcription, file_path)

        self.logger.info(f"Transcription of {file_path} is done")
        return transcription

    def save_transcription(self, transcription, file_path):
        transcription_path = file_path.parent / f"{file_path.stem}.txt"

        with transcription_path.open("w", encoding="utf-8") as f:
            for sentence in transcription:
                f.write(
                    f"{sentence['start']} - {sentence['end']}\n{sentence['text']}\n\n"
                )

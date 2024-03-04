import logging
import torch
import whisper


class AudioExtractor:
    def __init__(self):
        print(torch.__version__)
        self.logger = logging.getLogger(__name__)
        self.setting = {"model": "medium", "device": self.is_cuda_available()}

        self.model = None

    def is_cuda_available(self):
        if torch.cuda.is_available():
            self.logger.info("CUDA is available")
            return "cuda"
        else:
            self.logger.info("CUDA is not available")
            return "cpu"

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

        with transcription_path.open("w") as f:
            for sentence in transcription:
                f.write(
                    f"{sentence['start']} - {sentence['end']}\n{sentence['text']}\n\n"
                )

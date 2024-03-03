import whisper
import pathlib


class AudioExtractor:
    def __init__(self):
        self.settings = {"model": "small", "device": "cpu"}
        self.model = None

    def load_model(self):
        self.model = whisper.load_model(
            name=self.settings["model"], device=self.settings["device"]
        )

    def extract_audio(self, audio_file):
        if not pathlib.Path(audio_file).exists():
            raise FileNotFoundError(f"File not found: {audio_file}")

        if self.model is None:
            self.model = self.load_model()

        transcription_list = self.transcribe_audio(audio_file)

        transcription_path = (
            pathlib.Path(audio_file).parent
            / f"{pathlib.Path(audio_file).stem}_transcription.txt"
        )

        self.save_transcription(transcription_list, transcription_path)
        return transcription_list

    def transcribe_audio(self, audio_file):
        loaded_audio = whisper.load_audio(audio_file)
        segments = self.model.transcribe(loaded_audio)["segments"]
        transcription_list = [
            {
                "start": sentence["start"],
                "end": sentence["end"],
                "text": str(sentence["text"]),
            }
            for sentence in segments
        ]
        return transcription_list

    def save_transcription(self, transcription, transcription_path):
        with pathlib.Path(transcription_path).open("w", encoding="utf-8") as file:
            for sentence in transcription:
                file.write(
                    f"{sentence['start']:.2f} ~ {sentence['end']:.2f}\n{sentence['text']}\n\n"
                )

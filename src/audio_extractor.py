import logging
import os

import toml
import whisper


class AudioExtractor:
    def __init__(self):
        self.models = ["small", "medium", "large"]
        self.model = None
        self.model_config = self.load_model_config()

    def load_model_config(self):
        with open("config.toml", "r") as f:
            config = toml.load(f)
            model = config["whisper"]["model"]
        return model

    def change_model_config(self, model):
        with open("config.toml", "r") as f:
            config = toml.load(f)

        config["whisper"]["model"] = model

        with open("config.toml", "w") as f:
            toml.dump(config, f)
            self.model_config = model

    def extract_transcription(self, file_path):
        if self.model is None or self.model_config != self.load_model_config():
            self.model = whisper.load_model(self.load_model_config())

        file_name = os.path.basename(file_path).split(".")[0]
        parent_folder_path = os.path.dirname(file_path)
        transcription_folder_path = os.path.join(parent_folder_path, "transcription")

        if not os.path.exists(transcription_folder_path):
            os.makedirs(transcription_folder_path, exist_ok=True)

        audio = whisper.load_audio(file_path)
        transcription = self.model.transcribe(audio)
        segment = transcription["segments"]

        transcription_dict = [
            {
                "start": round(sentence["start"], 2),
                "end": round(sentence["end"], 2),
                "text": sentence["text"],
            }
            for sentence in segment
        ]

        try:
            with open(
                os.path.join(transcription_folder_path, f"{file_name}.txt"), "w"
            ) as f:
                for sentence in transcription_dict:
                    f.write(
                        f"{sentence['start']} ~ {sentence['end']} \n{sentence['text']}\n\n"
                    )
        except Exception as exc:
            error_msg = f"Failed to make transcription file from {file_path}: {exc}"
            logging.error(error_msg)

        return transcription_dict

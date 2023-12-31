import logging
import os

import toml
import whisper


class AudioExtractor:
    def __init__(self):
        self.models = ["small", "medium", "large"]
        self.current_model = self.load_model_config()
        self.last_model = self.current_model
        self.model = whisper.load_model(self.current_model)

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
            self.current_model = model

    def extract_transcription(self, file_path):
        if self.current_model != self.last_model:
            self.model = whisper.load_model(self.current_model)
            self.last_model = self.current_model

        file_name = os.path.basename(file_path).split(".")[0]
        parent_folder_path = os.path.dirname(file_path)

        try:
            audio = whisper.load_audio(file_path)
        except Exception as exc:
            error_msg = f"Failed to load audio from {file_path}: {exc}"
            logging.error(error_msg)
            return
        try:
            transcription = self.model.transcribe(audio)
        except Exception as exc:
            error_msg = f"Failed to transcribe audio from {file_path}: {exc}"
            logging.error(error_msg)
            return

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
                os.path.join(parent_folder_path, f"{file_name}_transcription.txt"), "w"
            ) as f:
                for sentence in transcription_dict:
                    f.write(
                        f"{sentence['start']} ~ {sentence['end']} \n{sentence['text']}\n\n"
                    )
        except Exception as exc:
            error_msg = f"Failed to make transcription file from {file_path}: {exc}"
            logging.error(error_msg)

        return transcription_dict

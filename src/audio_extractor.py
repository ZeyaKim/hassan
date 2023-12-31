import logging
import os

import toml
import whisper
import torch

class AudioExtractor:
    def __init__(self):
        self.models = ["small", "medium", "large"]
        self.current_model = self.load_model_config()
        self.last_model = self.current_model
        self.model = None

    def load_model_config(self):
        logging.info("Loading model configuration")
        with open("config.toml", "r") as f:
            config = toml.load(f)
            model = config["whisper"]["model"]
        return model

    def change_model_config(self, model):
        logging.info(f"Changing model configuration to {model}")
        with open("config.toml", "r") as f:
            config = toml.load(f)

        config["whisper"]["model"] = model

        with open("config.toml", "w") as f:
            toml.dump(config, f)
            self.current_model = model
            logging.info(f"Model configuration updated to {model}")

    def extract_transcription(self, file_path):
        logging.info(f"Starting transcription for {file_path}")
        if self.current_model != self.last_model or self.model is None:
            try:
                logging.info(f'Checking cuda device: {torch.cuda.get_device_name()}')
                logging.info(f"Loading Whisper model: {self.current_model}")
                self.model = whisper.load_model(self.current_model, device="cuda")
                self.last_model = self.current_model
            except Exception as exc:
                error_msg = f"Failed to load Whisper model: {exc}"
                logging.error(error_msg)
                return
            
        whisper.available_models()
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        parent_folder_path = os.path.dirname(file_path)

        try:
            logging.info(f"Loading audio file: {file_path}")
            audio = whisper.load_audio(file_path)
        except Exception as exc:
            error_msg = f"Failed to load audio from {file_path}: {exc}"
            logging.error(error_msg)
            return
        try:
            logging.info("Transcribing audio")
            transcription = self.model.transcribe(audio, fp16=False)
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
            transcription_file_path = os.path.join(
                parent_folder_path, f"{file_name}_transcription.txt"
            )
            logging.info(f"Writing transcription to {transcription_file_path}")
            with open(transcription_file_path, "w") as f:
                for sentence in transcription_dict:
                    f.write(
                        f"{sentence['start']} ~ {sentence['end']}\n{sentence['text']}\n"
                    )
            logging.info("Transcription successfully saved")
        except Exception as exc:
            error_msg = f"Failed to save transcription file for {file_path}: {exc}"
            logging.error(error_msg)

        return transcription_dict

import logging
import os

import toml
import pysubs2


class SubtitleGenerator:
    def __init__(self):
        self.subs_exts = ["srt", "ass"]
        self.ext = self.load_subtitle_ext()

    def create_event(self, sentence):
        start_second, start_ms = map(int, str(sentence["start"]).split("."))
        end_second, end_ms = map(int, str(sentence["end"]).split("."))
        text = sentence["translated_text"]

        return pysubs2.SSAEvent(
            start=pysubs2.make_time(s=start_second, ms=start_ms),
            end=pysubs2.make_time(s=end_second, ms=end_ms),
            text=text,
        )

    def load_subtitle_ext(self):
        with open("config.toml", "r") as f:
            config = toml.load(f)
            subtitle_ext = config['pysubs2']['subtitle_ext']
        return subtitle_ext

    def edit_subtitle_ext(self, subtitle_ext):
        if subtitle_ext in self.subs_exts:
            with open("config.toml", "r") as f:
                config = toml.load(f)
            config['pysubs2']['subtitle_ext'] = subtitle_ext
            with open("config.toml", "w") as f:
                toml.dump(config, f)
                self.ext = subtitle_ext

    def generate_subtitle(self, file_path, translated_transcription):
        logging.info(f"Starting subtitle generation for {file_path}")
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        parent_folder_path = os.path.dirname(file_path)

        subs = pysubs2.SSAFile()

        try:
            for sentence in translated_transcription:
                subs.append(self.create_event(sentence))

            subs_path = os.path.join(parent_folder_path, f"{file_name}.{self.ext}")
            subs.save(
                subs_path,
                encoding="utf-8",
            )
            logging.info(f"Subtitle successfully generated at {subs_path}")

        except Exception as exc:
            logging.error(f"Error while generating subtitle for {file_path}: {exc}")

        logging.info(f"Subtitle is generated at {parent_folder_path}")

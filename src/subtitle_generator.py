import logging
import os

import pysubs2


class SubtitleGenerator:
    def __init__(self):
        self.subs_exts = ["srt", "ass"]
        self.cur_ext = "ass"

    def create_event(self, sentence):
        start_second, start_ms = map(int, str(sentence["start"]).split("."))
        end_second, end_ms = map(int, str(sentence["end"]).split("."))
        text = sentence["translated_text"]

        return pysubs2.SSAEvent(
            start=pysubs2.make_time(s=start_second, ms=start_ms),
            end=pysubs2.make_time(s=end_second, ms=end_ms),
            text=text,
        )

    def generate_subtitle(self, file_path, translated_transcription):
        logging.info(f"Starting subtitle generation for {file_path}")
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        parent_folder_path = os.path.dirname(file_path)

        subs = pysubs2.SSAFile()

        try:
            for sentence in translated_transcription:
                subs.append(self.create_event(sentence))

            subs_path = os.path.join(parent_folder_path, f"{file_name}.{self.cur_ext}")
            subs.save(
                subs_path,
                encoding="utf-8",
            )
            logging.info(f"Subtitle successfully generated at {subs_path}")

        except Exception as exc:
            logging.error(f"Error while generating subtitle for {file_path}: {exc}")

        logging.info(f"Subtitle is generated at {parent_folder_path}")

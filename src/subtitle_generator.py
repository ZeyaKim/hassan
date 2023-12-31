import pysubs2
import logging
import os


class SubtitleGenerator:
    def __init__(self):
        self.subs_exts = ["srt", "ass"]
        self.cur_ext = "srt"

    def generate_subtitle(self, file_path, translated_transcription):
        file_name = os.path.basename(file_path).split(".")[0]
        parent_folder_path = os.path.dirname(file_path)

        subs = pysubs2.SSAFile()
        try:
            for sentence in translated_transcription:
                start_second, start_ms = map(int(sentence["start"].split(".")))
                end_second, end_ms = map(int(sentence["end"].split(".")))
                text = sentence["text"]

                subs.append(
                    pysubs2.SSAEvent(start=pysubs2.make_time(s=start_second,
                                                             ms=start_ms),
                                     end=pysubs2.make_time(s=end_second,
                                                           ms=end_ms),
                                     text=text))
            subs.save(os.path.join(parent_folder_path, f'{file_name}.{self.cur_ext}'), encoding="utf-8")

        except Exception as exc:
            logging.error(f"Erorr occured while generating subtitle: {exc}")

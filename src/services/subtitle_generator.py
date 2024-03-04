import logging
import pysubs2
import math


class SubtitleGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setting = {
            "extension": ".srt",
        }

    def create_subtitle(self, translated_transcription, file_path):
        subtitle_path = file_path.parent / (file_path.stem + self.setting["extension"])

        subs = pysubs2.SSAFile()

        try:
            for sentence in translated_transcription:
                start_ms, start_s = math.modf(sentence["start"])
                end_ms, end_s = math.modf(sentence["end"])

                line = pysubs2.SSAEvent(
                    start=pysubs2.make_time(s=start_s, ms=int(start_ms * 1000)),
                    end=pysubs2.make_time(s=end_s, ms=int(end_ms * 1000)),
                    text=sentence["translated_text"],
                )
                subs.append(line)

            subs.save(str(subtitle_path))

        except Exception as e:
            self.logger.error(f"Failed to create subtitle: {e}")

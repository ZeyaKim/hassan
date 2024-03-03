import logging
import pysubs2


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
            with subtitle_path.open("w", encoding="utf-8") as f:
                for sentence in translated_transcription:
                    line = pysubs2.SSAEvent(
                        start=round(sentence["start"], 2),
                        end=round(sentence["end"], 2),
                        text=sentence["translated_text"],
                    )
                    subs.append(line)
                subs.save(f)
        except Exception as e:
            self.logger.error(f"Failed to create subtitle: {e}")

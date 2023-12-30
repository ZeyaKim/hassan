import toml
import whisper

class AudioExtractor:
    def __init__(self):
        self.models = ['small', 'medium', 'large']
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
            
    def extract_audios(self, file_path):
        if self.model is None or self.model_config != self.load_model_config():
            self.model = whisper.load_mode(self.load_model_config())

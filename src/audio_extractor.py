import toml

class AudioExtractor:
    def __init__(self, audio_path):
        self.models = ['small', 'medium', 'large']
        
        
    def load_model_config(self):
        with open("config.toml", "r") as f:
            config = toml.load(f)
            model = config["model"]["audio"]
        return model

    def change_model_config(self, model):
        with open("config.toml", "rw") as f:
            config = toml.load(f)
            config["model"]["audio"] = model
            toml.dump(config, f)
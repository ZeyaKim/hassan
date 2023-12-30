import toml

class AudioExtractor:
    def __init__(self):
        self.models = ['small', 'medium', 'large']
        
    def load_model_config(self):
        with open("config.toml", "r") as f:
            config = toml.load(f)
            model = config["model"]["audio"]
        return model

    def change_model_config(self, model):
        with open("config.toml", "r") as f:
            config = toml.load(f)
            
        config["model"]["audio"] = model
        
        with open("config.toml", "w") as f:
            toml.dump(config, f)
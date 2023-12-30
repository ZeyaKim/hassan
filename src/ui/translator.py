import toml
import deepl
import logging

class Translator:
    def __init__(self):  
        ...
        
    def load_api_key(self):
        with open("keys.toml", "r") as f:
            config = toml.load(f)
            api_key = config["api_key"]["deepl"]
        return api_key
    
    def is_valid_api_key(self, api_key):
        try:
            translator = deepl.Translator(api_key)
            original_text = "바퀴"
            text_translated = translator.translate_text(original_text, "EN")
            if str(text_translated).isalpha():
                return True
        except Exception as exc:
            logging.error(exc)
            return False
        return False
    
    def edit_api_key(self, new_api_key):
        if self.is_valid_api_key(new_api_key):
            config = toml.load("keys.toml")
            config["api_key"]["deepl"] = new_api_key
            with open("keys.toml", "w") as f:
                toml.dump(config, f)
            return True
        else:
            logging.info("Invalid API key")
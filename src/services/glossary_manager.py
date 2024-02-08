import os
import toml

class GlossaryManager:
    def __init__(self, root_dir: str):
        self.glossary_dir_path = os.path.join(root_dir, "glossary")
        if not os.path.exists(self.glossary_dir_path):
            os.makedirs(self.glossary_dir_path)
        
    def get_glossary(self, source_lang: str, target_lang: str) -> None:
        if not os.path.exists(os.path.join(self.glossary_dir_path, self.glossary_file_name(source_lang, target_lang))):
            self.create_glossary(source_lang, target_lang)
        
    def glossary_file_name(self, source_lang: str, target_lang: str) -> str:
        return f"from_{source_lang}_to_{target_lang}.txt"
    
    def create_glossary(source_lang, target_lang) -> None:
        pass
    
    def load_glossary(self, source_lang, target_lang) -> None:
        with open(os.path.join(self.glossary_dir_path, self.glossary_file_name(source_lang, target_lang)), "r") as f:
            glossary = toml.load(f)
    
        return glossary
    
    def save_glossary(self, source_lang, target_lang) -> None:
        pass
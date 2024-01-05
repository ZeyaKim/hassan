from PySide6.QtWidgets import QVBoxLayout

class PathPanel(QVBoxLayout):
    def __init__(self) -> None:
        super().__init__()
        self.init_ui()
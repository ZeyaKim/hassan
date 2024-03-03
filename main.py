from PyQt5.QtWidgets import QApplication
from src.gui.main_window import MainWindow
import sys
import os
import pathlib

main_path = __file__
root_dir = os.environ["ROOT_DIR"] = str(pathlib.Path(main_path).parent.absolute())


def start_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    start_app()

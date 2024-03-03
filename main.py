from PySide6.QtWidgets import QApplication, QMainWindow


def start_app():
    app = QApplication()
    window = QMainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    start_app()

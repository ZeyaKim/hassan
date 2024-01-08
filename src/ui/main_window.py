import logging

from dependency_injector import containers, providers
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QPlainTextEdit,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from src.audio_extractor import AudioExtractor
from src.subtitle_generator import SubtitleGenerator
from src.translator import Translator

from .path_panel import PathPanel
from .setting_panel import SettingPanel


class Container(containers.DeclarativeContainer):
    translator = providers.Singleton(Translator)
    audio_extractor = providers.Singleton(AudioExtractor)
    subtitle_generator = providers.Singleton(SubtitleGenerator)
    log_viewer = providers.Singleton(QPlainTextEdit)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self) -> None:
        self.setWindowIcon(QIcon("assets/icon/hassan_icon.png"))
        self.setWindowTitle("Work Hard Hassan!")
        self.setGeometry(100, 100, 1080, 720)

        container = Container()

        path_panel = PathPanel(
            container.log_viewer(),
        )

        setting_panel = SettingPanel(
            container.audio_extractor(),
            container.translator(),
            container.subtitle_generator(),
            container.log_viewer(),
        )

        log_viewer = container.log_viewer()

        layout = QVBoxLayout()

        layout.addWidget(path_panel)
        layout.addWidget(setting_panel)
        layout.addWidget(log_viewer)

        widget_container = QWidget()
        widget_container.setLayout(layout)
        self.setCentralWidget(widget_container)

        self.create_tray_icon()

    def create_tray_icon(self) -> None:
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("assets/icon/hassan_icon.png"))

        tray_menu = QMenu()
        show_action = QAction("보기", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)

        exit_action = QAction("종료", self)
        exit_action.triggered.connect(QApplication.instance().quit)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def closeEvent(self, event) -> None:
        if QApplication.activeWindow() is not None:
            self.tray_icon.showMessage(
                "Work Hard Hassan!", "하산이 야근하고 있습니다!", QSystemTrayIcon.Information, 2000
            )
        event.ignore()
        self.hide()

    def add_log(self, message, log_level) -> None:
        match log_level:
            case "info":
                logging.info(message)
            case "error":
                logging.error(message)
        self.log_viewer.appendPlainText(message)

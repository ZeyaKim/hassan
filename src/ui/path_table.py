import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QHeaderView, QMenu, QTableWidget, QTableWidgetItem


class PathTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setColumnCount(2)  # 두 개의 열 설정
        self.setHorizontalHeaderLabels(["경로", "타입"])
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # 첫 번째 열을 가용 공간에 맞춤
        header.setSectionResizeMode(1, QHeaderView.Fixed)  # 두 번째 열의 크기를 고정
        self.setColumnWidth(1, 100)

    def add_new_path(self, new_path, path_type):
        rowCount = self.rowCount()
        for i in range(rowCount):
            if self.item(i, 0) and self.item(i, 0).text() == new_path:
                logging.info(f"Path {new_path} is already added")
                return

        self.insertRow(rowCount)
        self.setItem(rowCount, 0, QTableWidgetItem(new_path))
        self.setItem(rowCount, 1, QTableWidgetItem(path_type))
        logging.info(f"Path {new_path} is added")

    def show_context_menu(self, position):
        menu = QMenu(self)
        delete_action = QAction("삭제", self)
        menu.addAction(delete_action)

        action = menu.exec(self.mapToGlobal(position))

        if action == delete_action:
            selected_row = self.currentRow()
            if selected_row != -1:
                self.removeRow(selected_row)

    def get_removed_redudant_paths(self):
        paths = [
            {"path": self.item(row, 0).text(), "type": self.item(row, 1).text()}
            for row in range(self.rowCount())
        ]

        filtered_paths = []
        for path in paths:
            if not any(
                path["path"] != other_path["path"]
                and path["path"].startswith(other_path["path"])
                for other_path in paths
            ):
                filtered_paths.append(path)
        print(filtered_paths)
        return filtered_paths

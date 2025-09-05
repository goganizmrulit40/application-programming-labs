import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow)

from main import ImageIterator


class ImageViewerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Просмотр датасета изображений")
        self.setGeometry(100, 100, 800, 600)

        self.iterator = None
        self.annotation_file = None
        self.folder_path = None

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)



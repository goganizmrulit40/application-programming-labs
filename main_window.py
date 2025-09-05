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

        '''-------------------------------------------'''

        source_group = QGroupBox("Источник данных")
        source_layout = QVBoxLayout()

        btn_layout = QHBoxLayout()

        self.select_annotation_btn = QPushButton("Выбрать файл аннотации")
        self.select_annotation_btn.clicked.connect(self.select_annotation_file)
        btn_layout.addWidget(self.select_annotation_btn)

        self.select_folder_btn = QPushButton("Выбрать папку с изображениями")
        self.select_folder_btn.clicked.connect(self.select_folder)
        btn_layout.addWidget(self.select_folder_btn)

        source_layout.addLayout(btn_layout)
        source_group.setLayout(source_layout)
        main_layout.addWidget(source_group)


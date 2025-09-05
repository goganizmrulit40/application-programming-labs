import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QGroupBox, QHBoxLayout, QPushButton, QLabel,
                             QFileDialog, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

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

        '''-------------------------------------------'''

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(400, 300)
        self.image_label.setText("Выберите источник данных и нажмите 'Следующее изображение'")
        self.image_label.setStyleSheet("border: 1px solid gray; background-color: #f0f0f0;")
        main_layout.addWidget(self.image_label)

        '''-------------------------------------------'''

        nav_layout = QHBoxLayout()

        self.next_btn = QPushButton("Следующее изображение")
        self.next_btn.clicked.connect(self.show_next_image)
        self.next_btn.setEnabled(False)
        nav_layout.addWidget(self.next_btn)

        main_layout.addLayout(nav_layout)

        '''-------------------------------------------'''

        self.info_label = QLabel("Готов к работе")
        self.info_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.info_label)


    def select_annotation_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл аннотации", "", "CSV Files (*.csv)"
        )

        if file_path:
            try:
                self.annotation_file = file_path
                self.folder_path = None
                self.iterator = ImageIterator(annotation_file=file_path)
                self.next_btn.setEnabled(True)
                self.info_label.setText(f"Загружен файл аннотации: {os.path.basename(file_path)}")
                self.show_next_image()
                
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файл аннотации: {str(e)}")


    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, "Выберите папку с изображениями"
        )

        if folder_path:
            try:
                self.folder_path = folder_path
                self.annotation_file = None
                self.iterator = ImageIterator(folder_path=folder_path)
                self.next_btn.setEnabled(True)
                self.info_label.setText(f"Загружена папка: {os.path.basename(folder_path)}")
                self.show_next_image()

            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить папку: {str(e)}")


    def show_next_image(self):
        if self.iterator:
            try:
                image_path = next(self.iterator)
                self.display_image(image_path)

            except StopIteration:
                self.info_label.setText("Достигнут конец датасета")
                self.next_btn.setEnabled(False)

            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить изображение: {str(e)}")


    def display_image(self, image_path):
        try:
            if not os.path.isabs(image_path) and self.annotation_file:
                annotation_dir = os.path.dirname(self.annotation_file)
                image_path = os.path.join(annotation_dir, image_path)

            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)

                if not pixmap.isNull():
                    scaled_pixmap = pixmap.scaled(
                        self.image_label.width() - 20,
                        self.image_label.height() - 20,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                    self.image_label.setPixmap(scaled_pixmap)
                else:
                    self.image_label.setText("Не удалось загрузить изображение")
            else:
                self.image_label.setText(f"Файл не найден: {image_path}")

        except Exception as e:
            self.image_label.setText(f"Ошибка загрузки: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageViewerApp()
    window.show()
    sys.exit(app.exec_())


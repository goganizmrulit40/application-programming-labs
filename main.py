import argparse
import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np


def parse_arguments():
    """
    Парсит аргументы командной строки
    :return: объект с распарсенными аргументами
    """
    parser = argparse.ArgumentParser(description='Обработка изображения')
    parser.add_argument('input_image', help='Путь к входному изображению')
    parser.add_argument('output_image', help='Путь для сохранения результата')

    return parser.parse_args()


def load_image(image_path):
    """
    Загружает изображение из файла с помощью OpenCV
    :param image_path: str, путь к файлу изображения
    :return: массив NumPy с данными изображения в формате BGR
    """
    image = cv2.imread(image_path)
    print("Успешная загрузка!")
    if image is None:
        raise ValueError(f"Не удалось загрузить изображение: {image_path}")
    return image


def print_image_info(image):
    """
    Выводит информацию о размере изображения
    :param image: массив NumPy, входное изображение
    :return: кортеж с информацией об изображении:
            - width (int): ширина изображения в пикселях
            - height (int): высота изображения в пикселях
            - channels (int): количество цветовых каналов
    """
    height, width = image.shape[:2]
    channels = image.shape[2] if len(image.shape) == 3 else 1
    print(f"Размер изображения: {width}x{height} пикселей")
    print(f"Количество каналов: {channels}")
    return width, height, channels


def building_color_histogram(image):
    return


if __name__ == "__main__":
    try:
        args = parse_arguments()

        print("Загрузка изображения...")
        image = load_image(args.input_image)

        print("\nИнформация об изображении:")
        print_image_info(image)

        print("\nПостроение гистограммы...")
        building_color_histogram(image)

    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
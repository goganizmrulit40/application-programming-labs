import argparse
import sys

import cv2


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


if __name__ == "__main__":
    try:
        args = parse_arguments()

        print("Загрузка изображения...")
        image = load_image(args.input_image)

    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
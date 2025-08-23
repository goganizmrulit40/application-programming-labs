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
    parser = argparse.ArgumentParser(
        description='Обработка изображения: гистограмма, размер и стыковка'
    )
    parser.add_argument('input_image', help='Путь к входному изображению')
    parser.add_argument('output_image', help='Путь для сохранения результата')
    parser.add_argument(
        '--second_image',
        help='Путь ко второму изображению для стыковки (опционально)'
    )
    parser.add_argument(
        '--grayscale',
        action='store_true',
        help='Принудительная загрузка в оттенках серого'
    )

    return parser.parse_args()


def load_image(image_path, grayscale=False):
    """
    Загружает изображение из файла с помощью OpenCV
    :param image_path: str, путь к файлу изображения
    :param grayscale: bool, загрузка в оттенках серого
    :return: массив NumPy с данными изображения
    """
    if grayscale:
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    else:
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
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
    """
    Строит и отображает цветную гистограмму для изображения
    :param image: массив NumPy, входное изображение
    :return: Гистограмма показывает распределение значений пикселей
            по каждому из цветовых каналов (синий, зеленый, красный)
            или по яркости пикселя в случае черно-белого изображения
    """

    if len(image.shape) == 2 or image.shape[2] == 1:
        plt.figure(figsize=(10, 5))
        hist = cv2.calcHist([image], [0], None, [256], [0, 256])
        plt.plot(hist, color='black', label='Яркость', alpha=0.7, linewidth=2)

        plt.title('Гистограмма яркости (черно-белое изображение)')
        plt.xlabel('Значение пикселя (яркость)')

    else:
        colors = ('b', 'g', 'r')
        channel_names = ('Синий', 'Зеленый', 'Красный')

        plt.figure(figsize=(10, 5))
        for i, color in enumerate(colors):
            hist = cv2.calcHist([image], [i], None, [256], [0, 256])
            plt.plot(hist, color=color, label=channel_names[i], alpha=0.7)

        plt.title('Гистограмма цветов изображения')
        plt.xlabel('Значение пикселя')

    plt.ylabel('Частота')
    plt.axhline(0, color='black', linewidth=0.5, ls='--')
    plt.axvline(0, color='black', linewidth=0.5, ls='--')
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    plt.legend()

    plt.show()
    print("Успешное построение гистограммы!")
    return


def display_image(image, title):
    """
    Отображает изображение с заголовком с помощью matplotlib
    :param image: массив NumPy, входное изображение
    :param title: str, заголовок для отображения
    :return: конвертирует из BGR (OpenCV) в RGB (matplotlib)
            для корректного отображения цветов,
            или отображает в оттенках серого
    """
    plt.figure(figsize=(10, 5))

    if len(image.shape) == 3:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.imshow(image_rgb)
    else:
        plt.imshow(image, cmap='gray')

    plt.title(title)
    plt.axis('off')
    plt.show()


def stitch_images(image1, image2):
    """
    Состыкует два изображения горизонтально с сохранением пропорций
    :param image1: массив NumPy, первое изображение (базовое)
    :param image2: массив NumPy, второе изображение (масштабируется к первому)
    :return: массив NumPy, результирующее изображение, состоящее из двух состыкованных
    """
    h1, w1 = image1.shape[:2]
    h2, w2 = image2.shape[:2]

    scale_factor = h1 / h2
    new_width = int(w2 * scale_factor)
    image2_resized = cv2.resize(image2, (new_width, h1))

    return np.hstack((image1, image2_resized))


def create_mirrored_image(image):
    """
    Создает зеркальное отражение изображения
    :param image: массив NumPy, входное изображение
    :return: массив NumPy, зеркально отраженное изображение
    """
    return cv2.flip(image, 1)


if __name__ == "__main__":
    try:
        args = parse_arguments()

        print("Загрузка изображения...")
        image = load_image(args.input_image, args.grayscale)

        print("\nИнформация об изображении:")
        print_image_info(image)

        print("\nПостроение гистограммы...")
        building_color_histogram(image)

        print("Отображение исходного изображения...")
        display_image(image, 'Исходное изображение')

        print("Состыковка изображений...")
        if args.second_image:
            second_image = load_image(args.second_image)
            stitched_image = stitch_images(image, second_image)
            result_title = 'Состыкованное изображение'
        else:
            mirrored_image = create_mirrored_image(image)
            stitched_image = stitch_images(image, mirrored_image)
            result_title = 'Стыкованное изображение (исходное + зеркальное)'

        display_image(stitched_image, result_title)

    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
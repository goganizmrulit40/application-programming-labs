import argparse
import sys


def parse_arguments():
    """
    Парсит аргументы командной строки
    :return: объект с распарсенными аргументами
    """
    parser = argparse.ArgumentParser(description='Обработка изображения')
    parser.add_argument('input_image', help='Путь к входному изображению')
    parser.add_argument('output_image', help='Путь для сохранения результата')

    return parser.parse_args()


if __name__ == "__main__":
    try:
        args = parse_arguments()

    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
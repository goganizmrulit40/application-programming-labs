import pandas as pd
import argparse


def parse_arguments():
    """
    Парсинг аргументов командной строки
    :return: объект с распарсенными аргументами
    """
    parser = argparse.ArgumentParser(description='Обработка данных изображений')

    parser.add_argument('-i', '--input', required=True,
                        help='Входной CSV файл с путями к изображениям')

    parser.add_argument('-o', '--output', default='processed_image_data.csv',
                        help='Выходной CSV файл (по умолчанию: processed_image_data.csv)')

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    print(f"Входной файл: {args.input}")
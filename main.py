import pandas as pd
import argparse
import sys


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


def load_and_rename_data(file_path):
    """
    Загружает данные из CSV файла и переименовывает колонки
    :param file_path: str, путь к CSV файлу с данными об изображениях
    :return: pandas.DataFrame, DataFrame с колонками 'absolute_path' и 'relative_path'
    """
    df = pd.read_csv(file_path)
    df.columns = ['absolute_path', 'relative_path']
    print(f"Успешно загружено {len(df)} записей из {file_path}")
    return df


if __name__ == "__main__":
    args = parse_arguments()

    print(f"Входной файл: {args.input}")

    input_file = args.input

    print("1. Загрузка и переименование данных...")
    df = load_and_rename_data(input_file)









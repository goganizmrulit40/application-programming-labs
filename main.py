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
    try:
        df = pd.read_csv(file_path)
        df.columns = ['absolute_path', 'relative_path']
        print(f"Успешно загружено {len(df)} записей из {file_path}")
        return df
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        sys.exit(1)


def display_dataframe_info(df, name="DataFrame"):
    """
    Отображает основную информацию о DataFrame
    :param df: pandas.DataFrame, DataFrame для анализа
    :param name: str, название DataFrame для вывода в сообщениях
    """
    print(f"\nИнформация о {name}:")
    print(f"Количество строк: {len(df)}")
    print(f"Количество столбцов: {len(df.columns)}")
    print(f"Столбцы: {list(df.columns)}")

    print(f"\nПервые 5 строк:")
    if not df.empty:
        print(df.head())


def get_image_dimensions(image_path):
    """
    Получает размеры изображения (высоту, ширину и количество каналов)
    :param image_path: str, абсолютный путь к файлу изображения
    :return: кортеж (height, width, channels)
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            print(f"Предупреждение: Не удалось прочитать изображение {image_path}")
            return None, None, None
        height, width, channels = image.shape
        return height, width, channels
    except Exception as e:
        print(f"Ошибка при чтении изображения {image_path}: {e}")
        return None, None, None


if __name__ == "__main__":
    args = parse_arguments()

    print(f"Входной файл: {args.input}")

    input_file = args.input

    print("1. Загрузка и переименование данных...")
    df = load_and_rename_data(input_file)
    display_dataframe_info(df, "исходном DataFrame")

    print("\n2. Добавление информации о размерах изображений...")








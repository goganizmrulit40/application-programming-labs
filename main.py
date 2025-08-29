import pandas as pd
import cv2
import matplotlib.pyplot as plt
import argparse
import sys


def parse_arguments():
    """
    Парсинг аргументов командной строки
    :return: объект с распарсенными аргументами
    """
    parser = argparse.ArgumentParser(
        description='Обработка данных изображений анализ размеров, фильтрация и визуализация'
    )

    parser.add_argument('-i', '--input', required=True,
                        help='Входной CSV файл с путями к изображениям')

    parser.add_argument('-o', '--output', default='processed_image_data.csv',
                        help='Выходной CSV файл (по умолчанию: processed_image_data.csv)')
    parser.add_argument('--max-width', type=int, default=10000,
                        help='Максимальная ширина для фильтрации (по умолчанию: 10000)')
    parser.add_argument('--max-height', type=int, default=10000,
                        help='Максимальная высота для фильтрации (по умолчанию: 10000)')

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


def add_dimensions_columns(df):
    """
    Добавляет в DataFrame колонки с размерами изображений
    :param df: pandas.DataFrame, исходный DataFrame с путями к изображениям
    :return: pandas.DataFrame,
                модифицированный DataFrame
                с колонками 'height', 'width', 'channels'
    """
    dimensions = []
    successful = 0
    failed = 0

    for abs_path in df['absolute_path']:
        height, width, channels = get_image_dimensions(abs_path)
        dimensions.append((height, width, channels))

        if height is not None and width is not None:
            successful += 1
        else:
            failed += 1

    df['height'] = [d[0] for d in dimensions]
    df['width'] = [d[1] for d in dimensions]
    df['channels'] = [d[2] for d in dimensions]

    print(f"Успешно обработано изображений: {successful}, не удалось: {failed}")
    return df


def calculate_statistics(df):
    """
    Вычисляет и выводит статистическую информацию о размерах изображений
    :param df: pandas.DataFrame,
                DataFrame с колонками 'height', 'width', 'channels'
    """
    print("Статистическая информация о размерах изображений:")
    print(f"Высота:\n{df['height'].describe()}")
    print(f"\nШирина:\n{df['width'].describe()}")
    print(f"\nКаналы:\n{df['channels'].describe()}")


def filter_by_max_size(df, max_width, max_height):
    """
    Фильтрует DataFrame по максимальным размерам изображения
    :param df: pandas.DataFrame, DataFrame с колонками 'width' и 'height'
    :param max_width: int, максимально допустимая ширина изображения
    :param max_height: int, максимально допустимая высота изображения
    :return: pandas.DataFrame, отфильтрованный DataFrame с изображениями,
             удовлетворяющими условиям
    """
    if max_width <= 0 or max_height <= 0:
        print("Предупреждение: Максимальные размеры должны быть положительными числами")
        return df

    original_count = len(df)

    mask = (df['width'] <= max_width) & (df['height'] <= max_height)
    df_filtered = df[mask].copy()

    df.drop(df.index, inplace=True)
    df = pd.concat([df, df_filtered], ignore_index=True)

    print(f"\nОтфильтровано изображений: {len(df)} из {original_count}")
    return df


def add_area_column(df):
    """
    Добавляет колонку с площадью изображения
    :param df: pandas.DataFrame, DataFrame с колонками 'width' и 'height'
    :return: pandas.DataFrame, DataFrame с добавленной колонкой 'area'
    """
    df['area'] = df['width'] * df['height']
    return df


def sort_by_area(df):
    """
    Сортирует DataFrame по площади изображения в возрастающем порядке
    :param df: pandas.DataFrame, DataFrame с колонкой 'area'
    :return: pandas.DataFrame, отсортированный DataFrame
    """
    return df.sort_values('area', ascending=True)


def plot_area_histogram(df):
    """
    Создает и отображает гистограмму распределения площадей изображений
    :param df: pandas.DataFrame, DataFrame с колонкой 'area'
    """
    plt.figure(figsize=(12, 8))
    plt.hist(df['area'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')

    plt.title('Распределение площадей изображений', fontsize=16, fontweight='bold')
    plt.xlabel('Площадь изображения (пиксели)', fontsize=12)
    plt.ylabel('Количество изображений', fontsize=12)

    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)

    plt.tight_layout()
    plt.show()


def save_processed_data(df, output_file):
    """
    Сохраняет обработанные данные в CSV файл
    :param df: pandas.DataFrame, DataFrame для сохранения
    :param output_file: str, путь к выходному CSV файлу
    """
    try:
        df.to_csv(output_file, index=False)
        print(f"Обработанные данные сохранены в файл: {output_file}")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")


if __name__ == "__main__":
    args = parse_arguments()

    print(f"Входной файл: {args.input}")

    input_file = args.input
    output_file = args.output
    max_width = args.max_width
    max_height = args.max_height

    print("1. Загрузка и переименование данных...")
    df = load_and_rename_data(input_file)
    display_dataframe_info(df, "исходном DataFrame")

    print("\n2. Добавление информации о размерах изображений...")
    df = add_dimensions_columns(df)
    display_dataframe_info(df, "DataFrame с размерами")

    print("\n3. Вычисление статистики...")
    calculate_statistics(df)

    print(f"\n4. Фильтрация по максимальным размерам ({max_width}x{max_height})...")
    df = filter_by_max_size(df, max_width, max_height)
    display_dataframe_info(df, "отфильтрованном DataFrame")

    print("\n5. Добавление столбца с площадью...")
    df = add_area_column(df)
    display_dataframe_info(df, "DataFrame с площадью")

    print("\n6. Сортировка по площади...")
    df = sort_by_area(df)
    display_dataframe_info(df, "отсортированном DataFrame")

    print("\n7. Создание гистограммы...")
    plot_area_histogram(df)

    print("\n8. Сохранение результатов...")
    save_processed_data(df, output_file)

    print("\nОбработка завершена успешно!")
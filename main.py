import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Скачивание изображений и создание аннотации'
    )
    parser.add_argument(
        '--keyword',
        type=str,
        required=True,
        help='Ключевое слово для поиска изображений (bird)'
    )
    parser.add_argument(
        '--output_dir',
        type=str,
        required=True,
        help='Путь к папке для сохранения изображений'
    )
    parser.add_argument(
        '--annotation_file',
        type=str,
        required=True,
        help='Путь к файлу аннотации CSV'
    )
    parser.add_argument(
        '--max_num',
        type=int,
        default=50,
        help='Максимальное количество изображений для загрузки (50-1000)'
    )

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_arguments()
import argparse
import os
from icrawler.builtin import GoogleImageCrawler


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

    if args.max_num < 50 or args.max_num > 1000:
        raise ValueError("Количество изображений должно быть от 50 до 1000")

    return args


def download_images(keyword, output_dir, max_num):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    google_crawler = GoogleImageCrawler(
        storage={'root_dir': output_dir},
        downloader_threads=4
    )

    filters = dict(
        size='large',
        type='photo',
        color='color'
    )

    google_crawler.crawl(
        keyword=keyword,
        max_num=max_num,
        min_size=(200, 200),
        overwrite=True,
        filters=filters
    )




if __name__ == "__main__":
    args = parse_arguments()

    print(f"Скачивание {args.max_num} изображений"
          f"по ключевому слову '{args.keyword}'...")
    download_images(args.keyword, args.output_dir, args.max_num)

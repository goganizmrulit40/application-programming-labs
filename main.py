import argparse
import csv
import os
import sys
from icrawler.builtin import GoogleImageCrawler


class ImageIterator:
    def __init__(self, annotation_file=None, folder_path=None):
        try:
            if annotation_file:
                self.images = []
                with open(annotation_file, mode='r',
                          encoding='utf-8-sig') as file:
                    reader = csv.reader(file)
                    next(reader, None)

                    for row in reader:
                        if len(row) > 1:
                            self.images.append(row[1])
                self.counter = 0

            elif folder_path:
                self.images = [
                    os.path.join(folder_path, f)
                    for f in os.listdir(folder_path)
                    if os.path.isfile(os.path.join(folder_path, f)) and
                    f.lower().endswith(('.png', '.jpg', '.jpeg'))
                ]
                self.counter = 0

            else:
                raise ValueError(
                    "Необходимо указать либо файл аннотации, либо путь к папке"
                )

        except Exception as e:
            print(f"Ошибка при инициализации итератора: {str(e)}")
            sys.exit(1)

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter < len(self.images):
            image_path = self.images[self.counter]
            self.counter += 1
            return image_path
        else:
            raise StopIteration

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
    try:
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
        return True

    except Exception as e:
        print(f"Ошибка при загрузке изображений: {str(e)}")
        return False


def create_annotation(output_dir, annotation_file):
    try:
        os.makedirs(os.path.dirname(annotation_file) or '.', exist_ok=True)

        images = [
            f for f in os.listdir(output_dir)
            if os.path.isfile(os.path.join(output_dir, f)) and
            f.lower().endswith(('.png', '.jpg', '.jpeg'))
        ]

        #print(images)

        if not images:
            print("Нет изображений для создания аннотации!")
            return False

        with open(annotation_file, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(["Absolute Path", "Relative Path"])
            for img in images:
                abs_path = os.path.abspath(os.path.join(output_dir, img))
                rel_path = os.path.relpath(
                    abs_path,
                    start=os.path.dirname(annotation_file)
                )
                writer.writerow([abs_path, rel_path])

        return True

    except Exception as e:
        print(f"Ошибка при создании аннотации: {str(e)}")
        return False


if __name__ == "__main__":
    try:
        args = parse_arguments()

        print(f"Скачивание {args.max_num} изображений"
              f"по ключевому слову '{args.keyword}'...")
        if not download_images(args.keyword, args.output_dir, args.max_num):
            sys.exit(1)

        print(f"Создание аннотации в файле {args.annotation_file}...")
        if not create_annotation(args.output_dir, args.annotation_file):
            sys.exit(1)

        print("\nДемонстрация работы итератора "
              "(первые 5 изображений из файла аннотации):")
        iterator = ImageIterator(annotation_file=args.annotation_file)
        for i, img_path in enumerate(iterator):
            print(f"{i + 1}. {img_path}")
            if i >= 4:
                break

        print("\nДемонстрация работы итератора "
              "(первые 5 изображений из папки):")
        iterator = ImageIterator(folder_path=args.output_dir)
        for i, img_path in enumerate(iterator):
            print(f"{i + 1}. {img_path}")
            if i >= 4:
                break

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        sys.exit(1)

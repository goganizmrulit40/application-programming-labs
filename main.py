import argparse
from datetime import datetime


def parse_arguments():
    """
    Парсит аргументы командной строки
    :return: str, имя файла, переданное как аргумент командной строки
    """
    parser = argparse.ArgumentParser(description='Парсинг текстового файла')
    parser.add_argument('filename', type=str, help='Название текстового файла')
    args = parser.parse_args()
    return args.filename


def read_from_file(filename):
    """
    Читает содержимое файла
    :param filename: str, путь к файлу для чтения
    :return: str, содержимое файла в виде строки
    """
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def calculate_age(birth_date):
    """
    Вычисляет возраст на основе даты рождения
    :param birth_date: str, дата рождения в формате 'DD.MM.YYYY'
    :return: int, возраст в годах
    """
    today = datetime.now()
    birth_date = datetime.strptime(birth_date, "%d.%m.%Y")
    # print(birth_date)
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


def count_people_in_age_range(text):
    """
    Подсчитывает количество людей в возрасте от 30 до 40 лет
    :param text: str, текст с информацией о людях (каждый человек на новой строке)
    :return: int, кол-во людей, подходящих под описание
    """
    people = text.split('\n')
    count = 0

    for person in people:
        lines = person.split('\n')
        for line in lines:
            if line.startswith('Дата рождения:'):
                birth_date = line.split(': ')[1].strip()
                #print(birth_date)
                try:
                    age = calculate_age(birth_date)
                    if 30 <= age <= 40:
                        count += 1
                except ValueError:
                    continue
                break

    return count


if __name__ == "__main__":
    filename = parse_arguments()
    try:
        text = read_from_file(filename)
        count = count_people_in_age_range(text)
        print(f"Количество людей в возрасте от 30 до 40 лет: {count}")

    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден.")
    except Exception as e:
        print(f"Ошибка: {e}")
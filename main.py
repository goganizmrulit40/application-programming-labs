import argparse
from datetime import datetime


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='Название текстового файла')
    args = parser.parse_args()
    return args.filename


def read_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def calculate_age(birth_date):
    today = datetime.now()
    birth_date = datetime.strptime(birth_date, "%d.%m.%Y")
    # print(birth_date)
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


def count_people_in_age_range(text):
    people = text.split('\n')
    count = 0

    for person in people:
        lines = person.split('\n')
        for line in lines:
            if line.startswith('Дата рождения:'):
                birth_date = line.split(': ')[1].strip()
                #print(birth_date)
                age = calculate_age(birth_date)

    return count


if __name__ == "__main__":
    filename = parse_arguments()
    text = read_from_file(filename)
    count = count_people_in_age_range(text)
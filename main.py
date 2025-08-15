import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='Название текстового файла')
    args = parser.parse_args()
    return args.filename


def read_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def count_people_in_age_range(text):
    people = text.split('\n')
    count = 0

    for person in people:
        lines = person.split('\n')
        for line in lines:
            if line.startswith('Дата рождения:'):
                birth_date = line.split(': ')[1].strip()
                #print(birth_date)


    return count


if __name__ == "__main__":
    filename = parse_arguments()
    text = read_from_file(filename)
    count = count_people_in_age_range(text)
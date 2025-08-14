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


if __name__ == "__main__":
    filename = parse_arguments()
    text = read_from_file(filename)
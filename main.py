import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='Название текстового файла')
    args = parser.parse_args()
    return args.filename


if __name__ == "__main__":
    filename = parse_arguments()
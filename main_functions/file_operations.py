import os


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Файл '{file_path}' не найден.")
        return None


def get_full_file_path(directory, file_name):
    full_file_path = os.path.join(directory, file_name)
    return full_file_path


def transcript_abbreviations(directory):
    abbreviations_file_path = get_full_file_path(directory, 'abbreviations.txt')
    abbreviations = {}
    with open(abbreviations_file_path, 'r') as abbreviations_file:
        for line in abbreviations_file:
            line = line.strip()
            if line:
                abbreviation, full_name, team = line.split("_")
                abbreviations[abbreviation] = (full_name, team)
    return abbreviations

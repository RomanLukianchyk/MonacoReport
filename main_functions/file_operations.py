import os
import datetime
from config import DATETIME_FORMAT


def read_file_values(file_path):
    values = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                racer_id, racer_datetime = parse_racer_line(line)
                if racer_id not in values:
                    values[racer_id] = racer_datetime
                else:
                    if racer_datetime < values[racer_id]:
                        values[racer_id] = racer_datetime
    return values


def parse_racer_line(line):
    racer_id = line[:3]
    racer_date = line[3:13]
    racer_time = line[14:]
    datetime_string = racer_date + '_' + racer_time
    racer_datetime = datetime.datetime.strptime(datetime_string, DATETIME_FORMAT)
    return racer_id, racer_datetime


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Файл '{file_path}' не найден.")


def get_full_file_path(directory, file_name):
    full_file_path = os.path.join(directory, file_name)
    return full_file_path


def read_abbreviation_file(directory):
    abbreviations_path = get_full_file_path(directory, "abbreviations.txt")
    abbreviations = {}

    with open(abbreviations_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                abbreviation, full_name, team = line.split('_')
                abbreviations[abbreviation] = (full_name, team)

    return abbreviations


def read_start_file(directory):
    start_path = get_full_file_path(directory, "start.txt")
    return read_file_values(start_path)


def read_end_file(directory):
    end_path = get_full_file_path(directory, "end.txt")
    return read_file_values(end_path)

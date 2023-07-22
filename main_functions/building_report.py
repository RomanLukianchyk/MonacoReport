import datetime
from file_operations import transcript_abbreviations, get_full_file_path


def get_driver_statistics(best_racers_list, driver_name):
    for racer_id, (time, full_name, team) in best_racers_list:
        if full_name.lower() == driver_name.lower():
            return f"Гонщик: {full_name}\nКоманда: {team}\nЛучшее время: {time}"
    return None


def parse_racer_line(line):
    racer_id = line[:3]
    racer_date = line[3:13]
    racer_time = line[15:]
    datetime_string = racer_date + '_' + racer_time
    datetime_format = "%Y-%m-%d_%H:%M:%S.%f"
    racer_datetime = datetime.datetime.strptime(datetime_string, datetime_format)
    return racer_id, racer_datetime


def read_file_values(file_path, values):
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                racer_id, racer_datetime = parse_racer_line(line)
                if racer_id not in values or racer_datetime < values[racer_id]:
                    values[racer_id] = racer_datetime


def build_report(directory):
    start_file_path = get_full_file_path(directory, 'start.txt')
    end_file_path = get_full_file_path(directory, 'end.txt')
    start_values = {}
    end_values = {}
    best_time_report = {}
    abbreviations = transcript_abbreviations(directory)

    read_file_values(start_file_path, start_values)
    read_file_values(end_file_path, end_values)

    for racer_id_report, time_report in start_values.items():
        if racer_id_report in end_values and time_report < end_values[racer_id_report]:
            formatted_time_report = time_report.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            full_name, team = abbreviations.get(racer_id_report, ("", ""))
            best_time_report[racer_id_report] = (formatted_time_report, full_name, team)

    best_time_report = sorted(best_time_report.items(), key=lambda x: x[1])

    return best_time_report


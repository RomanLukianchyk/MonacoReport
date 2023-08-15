import datetime
from file_operations import transcript_abbreviations, get_full_file_path


def get_driver_statistics(best_racers_list, driver_name):
    for racer_id, (time, full_name, team) in best_racers_list.items():
        if full_name.lower() == driver_name.lower():
            return {
                'name': full_name,
                'team': team,
                'time': time
            }
    return None


def parse_racer_line(line):
    racer_id = line[:3]
    racer_date = line[3:13]
    racer_time = line[14:]
    datetime_string = racer_date + '_' + racer_time
    datetime_format = "%Y-%m-%d_%H:%M:%S.%f"
    racer_datetime = datetime.datetime.strptime(datetime_string, datetime_format)
    return racer_id, racer_datetime


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


def build_report(directory, driver_name=None, sort_order="asc"):
    start_file_path = get_full_file_path(directory, 'start.txt')
    end_file_path = get_full_file_path(directory, 'end.txt')
    abbreviations = transcript_abbreviations(directory)

    if driver_name and driver_name.lower() in [name.lower() for name, _ in abbreviations.values()]:
        abbreviations = {k: v for k, v in abbreviations.items() if v[0].lower() == driver_name.lower()}

    start_values = read_file_values(start_file_path)
    end_values = read_file_values(end_file_path)

    best_time_report = {}

    for racer_id_report, time_report in start_values.items():
        if racer_id_report in end_values and time_report < end_values[racer_id_report]:
            formatted_time_report = time_report.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            full_name, team = abbreviations.get(racer_id_report, ("", ""))
            best_time_report[racer_id_report] = (formatted_time_report, full_name, team)

    if driver_name is None:
        if sort_order == "asc":
            best_time_report = sorted(best_time_report.items(), key=lambda x: x[1])
        elif sort_order == "desc":
            best_time_report = sorted(best_time_report.items(), key=lambda x: x[1], reverse=True)

    if driver_name:
        driver_stats = get_driver_statistics(best_time_report, driver_name)
        if driver_stats:
            return best_time_report, driver_stats
        else:
            return None, None
    else:
        return best_time_report, None

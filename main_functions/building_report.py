from file_operations import read_start_file, read_abbreviation_file, read_end_file


def get_driver_statistics(best_racers_list, driver_key):
    time, full_name, team = best_racers_list[driver_key]
    return {
        'name': full_name,
        'team': team,
        'time': time
    }


def find_driver(abbreviations, driver_name):
    for abbreviation, (full_name, _) in abbreviations.items():
        if full_name == driver_name:
            return abbreviation, full_name


def build_report(directory, driver_name=None, sort_order="asc"):
    abbreviations = read_abbreviation_file(directory)
    start_values = read_start_file(directory)
    end_values = read_end_file(directory)

    best_time_report = {}

    if driver_name:
        found_driver = False
        for driver_key, (full_name, team) in abbreviations.items():
            time_report = start_values.get(driver_key)
            if driver_key in end_values and time_report >= end_values[driver_key]:
                best_time_report[driver_key] = ("ERROR!", full_name, team)
            else:
                formatted_time_report = time_report.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                best_time_report[driver_key] = (formatted_time_report, full_name, team)
        if not found_driver:
            return {}, None
        else:
            driver_key = next(iter(best_time_report))
            driver_stats = get_driver_statistics(best_time_report, driver_key)
            return best_time_report, driver_stats
    else:
        for driver_key, (full_name, team) in abbreviations.items():
            time_report = start_values.get(driver_key)
            if driver_key in end_values and time_report >= end_values[driver_key]:
                best_time_report[driver_key] = ("ERROR!", full_name, team)
            else:
                formatted_time_report = time_report.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                best_time_report[driver_key] = (formatted_time_report, full_name, team)

        best_time_report = dict(sorted(best_time_report.items(), key=lambda x: x[1], reverse=(sort_order == "desc")))
        return best_time_report, None

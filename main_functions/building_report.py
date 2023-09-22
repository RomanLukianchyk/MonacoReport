from main_functions.file_operations import read_start_file, read_abbreviation_file, read_end_file


class FoundingDriverError(Exception):
    def __init__(self, driver_name):
        self.driver_name = driver_name
        self.messege = f"Гонщик с именем '{driver_name}' не найден."
        super().__init__(self.messege)


def find_driver(abbreviations, driver_name):
    for abbreviation, (full_name, _) in abbreviations.items():
        if full_name == driver_name:
            return abbreviation, full_name
    raise FoundingDriverError(driver_name)


def build_report(directory, driver_name=None, sort_order="asc"):
    abbreviations = read_abbreviation_file(directory)
    start_values = read_start_file(directory)
    end_values = read_end_file(directory)

    if driver_name:

        driver_key, full_name = find_driver(abbreviations, driver_name)
        abbreviations = {driver_key: (full_name, abbreviations[driver_key][1])}

    best_time_report = {}
    invalid_racers_report = {}

    for driver_key, (full_name, team) in abbreviations.items():
        time_report = start_values.get(driver_key)
        if driver_key in end_values and time_report >= end_values[driver_key]:
            invalid_racers_report[driver_key] = ("ERROR! Время финиша меньше времени старта", full_name, team)
        else:
            formatted_time_report = time_report.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            best_time_report[driver_key] = (formatted_time_report, full_name, team)

    best_time_report = dict(sorted(best_time_report.items(), key=lambda x: x[1], reverse=(sort_order == "desc")))
    return best_time_report, invalid_racers_report

from file_operations import read_start_file, read_abbreviation_file, read_end_file


def get_driver_statistics(best_racers_list, driver_name):
    for racer_id, (time, full_name, team) in best_racers_list.items():
        if full_name == driver_name:
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

    for racer_id_report, time_report in start_values.items():
        if racer_id_report in end_values:
            if time_report >= end_values[racer_id_report]:
                # formatted_time_report = time_report.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                full_name, team = abbreviations.get(racer_id_report, ("", ""))
                best_time_report[racer_id_report] = ("ERROR!", full_name, team)
            else:
                formatted_time_report = time_report.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                full_name, team = abbreviations.get(racer_id_report, ("", ""))
                best_time_report[racer_id_report] = (formatted_time_report, full_name, team)

    if driver_name:
        driver_stats = get_driver_statistics(best_time_report, driver_name)
        if driver_stats:
            return best_time_report, driver_stats
        else:
            return best_time_report, None
    else:
        if sort_order == "asc":
            best_time_report = dict(sorted(best_time_report.items(), key=lambda x: x[1]))
        elif sort_order == "desc":
            best_time_report = dict(sorted(best_time_report.items(), key=lambda x: x[1], reverse=True))
        return best_time_report, None

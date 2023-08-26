import sys
from config import NUM_TOP_RACERS


def format_racer_info(index, full_name, team, time):
    return f"{index}. {full_name.ljust(20)} | {team.ljust(30)}| {time}"


def print_report(best_racers_list, driver_stats=None):
    if not best_racers_list:
        print("Нет лучших гонщиков.")
        sys.exit()

    if driver_stats:
        full_name = driver_stats.get('name', "")
        team = driver_stats.get('team', "")
        time = driver_stats.get('time', "")

        print(format_racer_info("", full_name, team, time))
        if time == "ERROR!":
            print(f"Лучшее время: {time} (Ошибка: время финиша меньше времени старта)")
    else:
        print("Лучшее время для каждого гонщика:")

        racers_to_print = [driver_stats] if driver_stats else best_racers_list.items()

        for index, (driver_key, (time, full_name, team)) in enumerate(racers_to_print, start=1):
            full_name = full_name if full_name else ""
            team = team if team else ""

            line = format_racer_info(index, full_name, team, time)
            if time == "ERROR!":
                line += " (Ошибка: время финиша меньше времени старта)"

            print(line)

            if index == NUM_TOP_RACERS:
                print("_" * 80)

import sys
from config import NUM_TOP_RACERS


def format_racer_info(index, full_name, team, time):
    return f"{index}. {full_name.ljust(20)} | {team.ljust(30)}| {time}"


def print_report(best_racers_list):
    if not best_racers_list:
        print("Нет лучших гонщиков.")
        sys.exit()

    print("Лучшее время для каждого гонщика:")

    for index, (driver_key, (time, full_name, team)) in enumerate(best_racers_list.items(), start=1):
        full_name = full_name if full_name else ""
        team = team if team else ""

        line = format_racer_info(index, full_name, team, time)
        if time == "ERROR!":
            line += " (Ошибка: время финиша меньше времени старта)"

        print(line)

        if index == NUM_TOP_RACERS:
            print("_" * 80)

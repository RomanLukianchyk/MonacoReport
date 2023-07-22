import sys


def print_report(best_racers_list):
    if not best_racers_list:
        print("Нет лучших гонщиков.")
        sys.exit()

    print("Лучшее время для каждого гонщика:")
    for index, (racer_id, (time, full_name, team)) in enumerate(best_racers_list, start=1):
        print(f"{index}. {full_name.ljust(20)}| {team.ljust(30)}| {time}")
        if index >= 10:
            break

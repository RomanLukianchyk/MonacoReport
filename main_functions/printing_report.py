import sys


def print_report(best_racers_list, driver_stats=None):
    if not best_racers_list:
        print("Нет лучших гонщиков.")
        sys.exit()

    if driver_stats:
        print(f"\nСтатистика для гонщика '{driver_stats['name']}':")
        print(f"Гонщик: {driver_stats['name']}")
        print(f"Команда: {driver_stats['team']}")
        print(f"Лучшее время: {driver_stats['time']}")
    else:
        print("Лучшее время для каждого гонщика:")
        for index, (racer_id, (time, full_name, team)) in enumerate(best_racers_list, start=1):
            print(f"{index}. {full_name.ljust(20)}| {team.ljust(30)}| {time}")
            if index >= 10:
                break

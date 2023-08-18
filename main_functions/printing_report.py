import sys


def print_report(best_racers_list, driver_stats=None):
    if not best_racers_list:
        print("Нет лучших гонщиков.")
        sys.exit()

    if driver_stats:
        full_name = driver_stats.get('name', "")
        team = driver_stats.get('team', "")
        time = driver_stats.get('time', "")

        print(f"\nСтатистика для гонщика '{full_name}':")
        print(f"Гонщик: {full_name}")
        print(f"Команда: {team}")
        if time == "ERROR!":
            print(f"Лучшее время: {time} (Ошибка: время финиша меньше времени старта)")
        else:
            print(f"Лучшее время: {time}")
    else:
        print("Лучшее время для каждого гонщика:")
        for index, (racer_id, (time, full_name, team)) in enumerate(best_racers_list.items(), start=1):
            full_name = full_name if full_name else ""
            team = team if team else ""

            if time == "ERROR!":
                print(f"{index}. {full_name.ljust(20)}| {team.ljust(30)}| {time} (Ошибка: время финиша меньше времени старта)")
            else:
                print(f"{index}. {full_name.ljust(20)}| {team.ljust(30)}| {time}")
            if index >= 10:
                break

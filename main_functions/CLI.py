import argparse
from building_report import build_report, get_driver_statistics
from printing_report import print_report


def main_cli():
    args = parse_arguments()

    if not args.files:
        print("Пожалуйста, укажите путь к папке с файлами start.txt и end.txt.")
        return

    print(f"Используем папку: {args.files}")

    directory = args.files
    best_racers_list = build_report(directory)

    if not best_racers_list:
        print("Нет данных для отчета.")
        return

    print_report(best_racers_list)

    if args.driver:
        driver_stats = get_driver_statistics(best_racers_list, args.driver)
        if driver_stats:
            print(f"Статистика для гонщика '{args.driver}':")
            print(driver_stats)
        else:
            print(f"Статистика для гонщика '{args.driver}' не найдена.")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Утилита для обработки отчетов о гонках на автодроме Монако")
    parser.add_argument("--files", help="Путь к папке с файлами start.txt и end.txt")
    parser.add_argument("--asc", action="store_true", help="Сортировать гонщиков по возрастанию времени (по умолчанию)")
    parser.add_argument("--desc", action="store_true", help="Сортировать гонщиков по убыванию времени")
    parser.add_argument("--driver", help="Показать статистику о конкретном гонщике")

    return parser.parse_args()

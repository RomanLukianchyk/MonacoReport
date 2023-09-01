import argparse
import sys

from building_report import build_report
from printing_report import print_report

def main_cli():
    args = parse_arguments()

    print(f"Используем папку: {args.files}")

    try:
        best_racers, invalid_racers = build_report(args.files, driver_name=args.driver, sort_order=args.sort_order)
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
        return

    if not best_racers:
        print("Лучшее время для каждого нщика:")
        print_report(invalid_racers)
        sys.exit()
    else:
        print("Лучшее время:")
        print_report(best_racers)
        print("Гонщики с неправильным временем:")
        print_report(invalid_racers)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Утилита для обработки отчетов о гонках на автодроме Монако")
    parser.add_argument("--files", help="Путь к папке с файлами start.txt и end.txt", required=True)
    parser.add_argument("--asc", action="store_const", const="asc", dest="sort_order", default="asc",
                        help="Сортировать гонщиков по возрастанию времени (по умолчанию)")
    parser.add_argument("--desc", action="store_const", const="desc", dest="sort_order",
                        help="Сортировать гонщиков по убыванию времени")
    parser.add_argument("--driver", help="Показать статистику о конкретном гонщике")

    return parser.parse_args()



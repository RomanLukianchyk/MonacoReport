import argparse
from building_report import build_report
from printing_report import print_report


def main_cli():
    args = parse_arguments()

    print(f"Используем папку: {args.files}")

    try:
        racers_report, _ = build_report(args.files, driver_name=args.driver, sort_order=args.sort_order)
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
        return

    if not racers_report:
        print("Нет данных для отчета.")
    elif args.driver and racers_report is None:
        print(f"Статистика для гонщика '{args.driver}' не найдена.")
    else:
        print_report(racers_report)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Утилита для обработки отчетов о гонках на автодроме Монако")
    parser.add_argument("--files", help="Путь к папке с файлами start.txt и end.txt", required=True)
    parser.add_argument("--asc", action="store_const", const="asc", dest="sort_order", default="asc",
                        help="Сортировать гонщиков по возрастанию времени (по умолчанию)")
    parser.add_argument("--desc", action="store_const", const="desc", dest="sort_order",
                        help="Сортировать гонщиков по убыванию времени")
    parser.add_argument("--driver", help="Показать статистику о конкретном гонщике")

    return parser.parse_args()



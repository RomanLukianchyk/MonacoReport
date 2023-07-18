import argparse
import sys
from main import build_report, print_report, get_driver_statistics

def parse_arguments():
    parser = argparse.ArgumentParser(description="Race Report CLI")
    parser.add_argument("--files", help="Path to the folder containing start.txt and end.txt files")
    parser.add_argument("--asc", action="store_true", help="Sort the racers in ascending order (default)")
    parser.add_argument("--desc", action="store_true", help="Sort the racers in descending order")
    parser.add_argument("--driver", help="Show statistics about a specific driver")

    return parser.parse_args()

def main():
    args = parse_arguments()

    if not args.files:
        print("Please provide the path to the folder containing start.txt and end.txt files.")
        return

    best_racers_list = build_report(args.files)

    if args.driver:
        driver_stats = get_driver_statistics(best_racers_list, args.driver)
        if driver_stats:
            print(f"Statistics for driver '{args.driver}':")
            print(driver_stats)
        else:
            print(f"No statistics found for driver '{args.driver}'.")
    else:
        if args.desc:
            best_racers_list.reverse()
        print_report(best_racers_list)


class PrintReportTestCase(unittest.TestCase):
    def test_print_report_with_data(self):
        best_racers_list = [('SVF', ('12:02:58.917', 'Sebastian Vettel', 'FERRARI')),
                            ('NHR', ('12:02:49.914', 'Nico Hulkenberg', 'RENAULT')),
                            ('FAM', ('12:13:04.512', 'Fernando Alonso', 'MCLAREN RENAULT'))]

        expected_output = "Best time for each racer:\n" \
                          "1. Sebastian Vettel    | FERRARI                     | 12:02:58.917\n" \
                          "2. Nico Hulkenberg     | RENAULT                     | 12:02:49.914\n" \
                          "3. Fernando Alonso     | MCLAREN RENAULT             | 12:13:04.512\n"

        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            print_report(best_racers_list)
            self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_print_report_with_empty_list(self):
        best_racers_list = []

        expected_output = "No best racers found.\n"

        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            with self.assertRaises(SystemExit):
                print_report(best_racers_list)
            self.assertEqual(mock_stdout.getvalue(), expected_output)
            self.assertEqual(sys.exit.called, True)

if __name__ == "__main__":
    main()

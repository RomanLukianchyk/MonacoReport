import unittest
import os
from io import StringIO
from unittest.mock import patch

from formula1.main import build_report, get_driver_statistics, print_report, transcript_abbreviations


class BuildReportTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = 'temp_folder'
        os.makedirs(self.temp_dir, exist_ok=True)

    def tearDown(self):
        for file_name in ['start.txt', 'end.txt', 'abbreviations.txt']:
            file_path = os.path.join(self.temp_dir, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
        os.rmdir(self.temp_dir)

    def test_build_report_with_existing_files(self):
        start_text = "SVF2018-05-24_12:02:58.917\nNHR2018-05-24_12:02:49.914\nFAM2018-05-24_12:13:04.512"
        end_text = "SVF2018-05-24_12:04:03.332\nNHR2018-05-24_12:04:02.979\nFAM2018-05-24_12:14:17.169"
        abbreviations_text = "SVF_Sebastian Vettel_FERRARI\nNHR_Nico Hulkenberg_RENAULT\nFAM_Fernando Alonso_MCLAREN RENAULT"
        with open(os.path.join(self.temp_dir, 'start.txt'), 'w') as start_file, \
                open(os.path.join(self.temp_dir, 'end.txt'), 'w') as end_file, \
                open(os.path.join(self.temp_dir, 'abbreviations.txt'), 'w') as abbreviations_file:
            start_file.write(start_text)
            end_file.write(end_text)
            abbreviations_file.write(abbreviations_text)

        best_racers_list = build_report(self.temp_dir)

        expected_result = [('VBM', ('02:00:00.000', 'Valtteri Bottas', 'MERCEDES')),
                           ('NHR', ('02:02:49.914', 'Nico Hulkenberg', 'RENAULT')),
                           ('KMH', ('02:02:51.003', 'Kevin Magnussen', 'HAAS FERRARI')),
                           ('SVF', ('02:02:58.917', 'Sebastian Vettel', 'FERRARI')),
                           ('KRF', ('02:03:01.250', 'Kimi RГ¤ikkГ¶nen', 'FERRARI')),
                           ('CSR', ('02:03:15.145', 'Carlos Sainz', 'RENAULT')),
                           ('MES', ('02:04:45.513', 'Marcus Ericsson', 'SAUBER FERRARI')),
                           ('RGH', ('02:05:14.511', 'Romain Grosjean', 'HAAS FERRARI')),
                           ('LSW', ('02:06:13.511', 'Lance Stroll', 'WILLIAMS MERCEDES')),
                           ('PGS', ('02:07:23.645', 'Pierre Gasly','SCUDERIA TORO ROSSO HONDA')),
                           ('CLS', ('02:09:41.921', 'Charles Leclerc', 'SAUBER FERRARI')),
                           ('SPF', ('02:12:01.035', 'Sergio Perez','FORCE INDIA MERCEDES')),
                           ('FAM', ('02:13:04.512', 'Fernando Alonso', 'MCLAREN RENAULT')),
                           ('DRR', ('02:14:12.054', 'Daniel Ricciardo','RED BULL RACING TAG HEUER')),
                           ('BHS', ('02:14:51.985', 'Brendon Hartley','SCUDERIA TORO ROSSO HONDA')),
                           ('SSW', ('02:16:11.648','Sergey Sirotkin','WILLIAMS MERCEDES')),
                           ('EOF', ('02:17:58.810', 'Esteban Ocon','FORCE INDIA MERCEDES')),
                           ('LHM', ('02:18:20.125', 'Lewis Hamilton', 'MERCEDES')),
                           ('SVM', ('02:18:37.735', 'Stoffel Vandoorne', 'MCLAREN RENAULT'))]
        self.assertEqual(best_racers_list, expected_result)

    def test_build_report_with_missing_files(self):
        best_racers_list = build_report(self.temp_dir)

        self.assertEqual(best_racers_list, [])

    def test_get_driver_statistics_with_existing_driver(self):
        driver_name = 'Sebastian Vettel'
        best_racers_list = [
            ('SVF', ('12:02:58.917', 'Sebastian Vettel', 'FERRARI')),
            ('NHR', ('12:02:49.914', 'Nico Hulkenberg', 'RENAULT')),
            ('FAM', ('12:13:04.512', 'Fernando Alonso', 'MCLAREN RENAULT'))
        ]

        driver_stats = get_driver_statistics(best_racers_list, driver_name)

        expected_result = "Гонщик: Sebastian Vettel\nКоманда: FERRARI\nЛучшее время: 12:02:58.917"
        self.assertEqual(driver_stats, expected_result)

    def test_get_driver_statistics_with_missing_driver(self):
        driver_name = 'Lewis Hamilton'
        best_racers_list = [
            ('SVF', ('12:02:58.917', 'Sebastian Vettel', 'FERRARI')),
            ('NHR', ('12:02:49.914', 'Nico Hulkenberg', 'RENAULT')),
            ('FAM', ('12:13:04.512', 'Fernando Alonso', 'MCLAREN RENAULT'))
        ]

        driver_stats = get_driver_statistics(best_racers_list, driver_name)

        self.assertIsNone(driver_stats)


class TranscriptAbbreviationsTests(unittest.TestCase):
    def setUp(self):
        self.temp_file_path = 'temp_file.txt'
        abbreviations_text = "DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER\nSVF_Sebastian Vettel_FERRARI\nLHM_Lewis Hamilton_MERCEDES"
        with open(self.temp_file_path, 'w') as temp_file:
            temp_file.write(abbreviations_text)

    def tearDown(self):
        os.remove(self.temp_file_path)

    def test_transcript_abbreviations(self):
        abbreviations = transcript_abbreviations()

        expected_result = {'BHS': ('Brendon Hartley', 'SCUDERIA TORO ROSSO HONDA'),
                           'CLS': ('Charles Leclerc', 'SAUBER FERRARI'),
                           'CSR': ('Carlos Sainz', 'RENAULT'),
                           'DRR': ('Daniel Ricciardo', 'RED BULL RACING TAG HEUER'),
                           'EOF': ('Esteban Ocon', 'FORCE INDIA MERCEDES'),
                           'FAM': ('Fernando Alonso', 'MCLAREN RENAULT'),
                           'KMH': ('Kevin Magnussen', 'HAAS FERRARI'),
                           'KRF': ('Kimi RГ¤ikkГ¶nen', 'FERRARI'),
                           'LHM': ('Lewis Hamilton', 'MERCEDES'),
                           'LSW': ('Lance Stroll', 'WILLIAMS MERCEDES'),
                           'MES': ('Marcus Ericsson', 'SAUBER FERRARI'),
                           'NHR': ('Nico Hulkenberg', 'RENAULT'),
                           'PGS': ('Pierre Gasly', 'SCUDERIA TORO ROSSO HONDA'),
                           'RGH': ('Romain Grosjean', 'HAAS FERRARI'),
                           'SPF': ('Sergio Perez', 'FORCE INDIA MERCEDES'),
                           'SSW': ('Sergey Sirotkin', 'WILLIAMS MERCEDES'),
                           'SVF': ('Sebastian Vettel', 'FERRARI'),
                           'SVM': ('Stoffel Vandoorne', 'MCLAREN RENAULT'),
                           'VBM': ('Valtteri Bottas', 'MERCEDES')}
        self.assertEqual(abbreviations, expected_result)


class PrintReportTestCase(unittest.TestCase):
    def test_print_report_with_data(self):
        best_racers_list = [('SVF', ('12:02:58.917', 'Sebastian Vettel', 'FERRARI')),
                            ('NHR', ('12:02:49.914', 'Nico Hulkenberg', 'RENAULT')),
                            ('FAM', ('12:13:04.512', 'Fernando Alonso', 'MCLAREN RENAULT'))]

        expected_output = "Best time for each racer:\n" \
                          "1. Sebastian Vettel    | FERRARI                       | 12:02:58.917\n" \
                          "2. Nico Hulkenberg     | RENAULT                       | 12:02:49.914\n" \
                          "3. Fernando Alonso     | MCLAREN RENAULT               | 12:13:04.512\n"

        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            print_report(best_racers_list)
            self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_print_report_with_empty_list(self):
        best_racers_list = []

        expected_output = "No best racers found.\n"

        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                print_report(best_racers_list)
            self.assertEqual(cm.exception.code, None)
            self.assertEqual(mock_stdout.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()

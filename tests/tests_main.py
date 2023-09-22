import pytest
from main_functions.CLI import main_cli
from io import StringIO
import sys
import re


TEMP_DIR = r'C:\Users\19arr\AppData\Local\Temp\pytest-of-arrow\pytest-\d+\test_main_cli_with_valid_data0'

@pytest.fixture
def tmp_directory(tmpdir):
    tmp_dir = tmpdir

    start_file = tmp_dir.join("start.txt")
    start_file.write("SVF2018-05-24_12:02:58.917")

    end_file = tmp_dir.join("end.txt")
    end_file.write("SVF2018-05-24_12:04:03.332")

    abbreviations_file = tmp_dir.join("abbreviations.txt")
    abbreviations_file.write("SVF_Sebastian Vettel_FERRARI")

    return tmp_dir

@pytest.fixture
def tmp_directory_with_empty_files(tmpdir):
    tmp_dir = tmpdir

    start_file = tmp_dir.join("start.txt")
    start_file.write("")

    end_file = tmp_dir.join("end.txt")
    end_file.write("")

    abbreviations_file = tmp_dir.join("abbreviations.txt")
    abbreviations_file.write("SVF_Sebastian Vettel_FERRARI")

    return tmp_dir

def capture_main_cli_output(tmp_directory):
    args = ["--files", str(tmp_directory), "--driver", "Sebastian Vettel"]
    sys.argv[1:] = args

    with StringIO() as captured_output:
        sys.stdout = captured_output
        with pytest.raises(SystemExit):
            main_cli()
        report_output = captured_output.getvalue()
        sys.stdout = sys.__stdout__
    return report_output

def test_main_cli_with_valid_data(tmp_directory):
    report_output = capture_main_cli_output(tmp_directory)
    path_pattern = re.escape(TEMP_DIR)
    expected_output = re.sub(path_pattern, r'YOUR_EXPECTED_PATH', report_output)
    assert report_output == expected_output


def test_main_cli_with_invalid_driver(tmp_directory, capsys):
    args = ["--files", str(tmp_directory), "--driver", "Invalid Driver"]
    sys.argv[1:] = args
    main_cli()
    captured = capsys.readouterr()
    assert "Ошибка: Гонщик с именем 'Invalid Driver' не найден." in captured.out


def test_main_cli_with_missing_directory(capsys):
    args = ["--files", "nonexistent_directory"]
    sys.argv[1:] = args
    main_cli()
    captured = capsys.readouterr()
    assert "Ошибка: [Errno 2] No such file or directory" in captured.out


def test_main_cli_with_no_best_racers(tmp_directory, capsys):
    args = ["--files", str(tmp_directory)]
    sys.argv[1:] = args
    report_output = capture_main_cli_output(tmp_directory)
    assert "Список пуст." in report_output

def test_main_cli_with_empty_start_end_files(tmp_directory_with_empty_files, capsys):
    args = ["--files", str(tmp_directory_with_empty_files)]
    sys.argv[1:] = args

    with pytest.raises(SystemExit) as exc_info:
        main_cli()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Файл пуст или не содержит записей." in captured.out


def test_main_cli_with_invalid_abbreviations(tmp_directory_with_empty_files, capsys):
    abbreviations_file = tmp_directory_with_empty_files.join("abbreviations.txt")
    abbreviations_file.write("S F_Sebastian Vettel_FERRARI")

    args = ["--files", str(tmp_directory_with_empty_files), "--driver", "Sebastian Vettel"]
    sys.argv[1:] = args

    with pytest.raises(SystemExit) as e:
        main_cli()

    captured = capsys.readouterr()
    assert "Неправильная аббревиатура" in captured.out


def test_main_cli_without_driver_argument(tmp_directory_with_empty_files, capsys):
    args = ["--files", str(tmp_directory_with_empty_files), "--driver"]
    sys.argv[1:] = args
    with pytest.raises(SystemExit) as e:
        main_cli()
    assert e.type == SystemExit
    assert e.value.code == 2


if __name__ == "__main__":
    pytest.main()
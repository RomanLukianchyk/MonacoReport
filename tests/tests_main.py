import pytest
from main_functions.building_report import build_report
from main_functions.printing_report import print_report
from main_functions.file_operations import transcript_abbreviations


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


def test_transcript_abbreviations(tmp_directory):
    abbreviations = transcript_abbreviations(tmp_directory)
    assert abbreviations == {"SVF": ("Sebastian Vettel", "FERRARI")}


def test_build_report_with_driver(tmp_directory):
    best_racers, driver_stats = build_report(tmp_directory, driver_name="Sebastian Vettel")
    assert best_racers == {"SVF": ("2018-05-24 12:02:58.917", "Sebastian Vettel", "FERRARI")}
    assert driver_stats == {"name": "Sebastian Vettel", "team": "FERRARI", "time": "2018-05-24 12:02:58.917"}


def test_print_report_with_no_driver(capsys):
    with pytest.raises(SystemExit) as exc_info:
        print_report({})
    assert exc_info.type == SystemExit
    assert "" in str(exc_info.value)
    captured = capsys.readouterr()
    assert "Нет лучших гонщиков.\n" in captured.out


def test_print_report_with_driver(capsys):
    best_racers = {"SVF": ("2018-05-24 12:02:58.917", "Sebastian Vettel", "FERRARI")}
    driver_stats = {"name": "Sebastian Vettel", "team": "FERRARI", "time": "2018-05-24 12:02:58.917"}

    print_report(best_racers, driver_stats)
    captured = capsys.readouterr()
    assert "Статистика для гонщика 'Sebastian Vettel':" in captured.out


def test_build_report_with_sort_desc(tmp_directory):
    best_racers = build_report(tmp_directory, sort_order="desc")
    assert best_racers == ([('SVF', ('2018-05-24 12:02:58.917', 'Sebastian Vettel', 'FERRARI'))], None)


if __name__ == "__main__":
    pytest.main()

import datetime

def transcript_abbreviations():
    abbreviations = {}
    with open('C:/Foxminded/data.t6/abbreviations.txt', 'r') as abbreviations_file:
        for line in abbreviations_file:
            line = line.strip()
            if line:
                abbreviation, full_name, team = line.split("_")
                abbreviations[abbreviation] = (full_name, team)
        return abbreviations

def build_report():
    start_values = {}
    end_values = {}
    best_time_report = {}
    abbreviations = transcript_abbreviations()

    with open('C:/Foxminded/data.t6/start.txt', 'r') as start:
        for line in start:
            line = line.strip()
            if line:
                racer1 = line
                racer_id_start = racer1[:3]
                racer_date_start = racer1[3:13]
                racer_time_start = racer1[15:]
                datetime_start_string = racer_date_start + '_' + racer_time_start
                datetime_format = "%Y-%m-%d_%H:%M:%S.%f"
                racer_datetime_start = datetime.datetime.strptime(datetime_start_string, datetime_format)
                if racer_id_start not in start_values or racer_datetime_start < start_values[racer_id_start]:
                    start_values[racer_id_start] = racer_datetime_start

    with open('C:/Foxminded/data.t6/end.txt', 'r') as end:
        for line in end:
            line = line.strip()
            if line:
                racer2 = line
                racer_id_end = racer2[:3]
                racer_date_end = racer2[3:13]
                racer_time_end = racer2[14:]
                datetime_end_string = racer_date_end + '_' + racer_time_end
                datetime_format = "%Y-%m-%d_%H:%M:%S.%f"
                racer_datetime_end = datetime.datetime.strptime(datetime_end_string, datetime_format)
                if racer_id_end not in end_values or racer_datetime_end < end_values[racer_id_end]:
                    end_values[racer_id_end] = racer_datetime_end

    for racer_id_report, time_report in start_values.items():
        if racer_id_report in end_values and time_report < end_values[racer_id_report]:
            formatted_time_report = time_report.strftime("%H:%M:%S.%f")[:-3] # добавить %Y-%m-%d | для вывода даты
            full_name, team = abbreviations.get(racer_id_report, ("", ""))
            best_time_report[racer_id_report] = (formatted_time_report, full_name, team)

    best_time_report = sorted(best_time_report.items(), key=lambda x: x[1])

    return best_time_report


if __name__ == "__main__":
    best_racers_list = build_report()
    print("Best time for each racer:")
    for index, (racer_id, (time, full_name, team)) in enumerate(best_racers_list, start=1):
        print(f"{index}. {full_name.ljust(20)}| {team.ljust(30)}| {time}")


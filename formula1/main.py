def build_report():
    start_values = {}
    end_values = {}
    best_time_report = {}

    with open('C:/Foxminded/data.t6/start.txt', 'r') as start:
        for line in start:
            line = line.strip()
            if line:
                racer1 = line
                racer_id_start = racer1[:3]
                racer_time_start = racer1[14:]
                if racer_time_start not in start_values or racer_time_start < start_values[racer_id_start]:
                    start_values[racer_id_start] = racer_time_start

    with open('C:/Foxminded/data.t6/end.txt', 'r') as end:
        for line in end:
            line = line.strip()
            if line:
                racer2 = line
                racer_id_end = racer2[:3]
                racer_time_end = racer2[14:]
                if racer_time_end not in end_values or racer_time_end < end_values[racer_id_end]:
                    end_values[racer_id_end] = racer_time_end

    for racer_id_report, time_report in start_values.items():
        if racer_id_report in end_values:
            if time_report < end_values[racer_id_report]:
                best_time_report[racer_id_report] = time_report

    best_time_report = sorted(best_time_report.items(), key=lambda x: x[1])

    return best_time_report


if __name__ == "__main__":
    best_racers_list = build_report()
    print("Best time for each racer:")
    for index, (racer_id, time) in enumerate(best_racers_list, start=1):
        print(f"{index}. {racer_id} {time}")

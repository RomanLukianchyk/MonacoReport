
def build_report():
    racers = {}
    with open('C:/Foxminded/data.t6/start.txt', 'r') as start:
        for line in start:
            racer1 = line[:3]
            time1 = line[14:]
            racers[racer1] = time1
    with open('C:/Foxminded/data.t6/end.txt', 'r') as end:
        for line in end:
            racer2 = line[:3]
            time2 = line[14:]
            racers[racer2] = time2



# abbreviations = open('C:/Foxminded/data.t6/abbreviations.txt', 'r')


if __name__ == "__main__":
    build_report()


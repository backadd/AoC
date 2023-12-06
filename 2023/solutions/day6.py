"""https://adventofcode.com/2023/day/6"""

from aoc_util.helper import read


def getInput(test: bool = False):
    # READ INPUT
    if test:
        data = read("./2023/inputs/6-test.txt").strip().split("\n")
    else:
        data = read("./2023/inputs/6.txt").strip().split("\n")
    # PARSE DATA
    parsed_data = dict()
    for line in data:
        parsed_data[line.split(":")[0]] = line.split(":")[1].split()

    return parsed_data


def check_value(value: int, time: int, distance: int):
    return value * (time - value) > distance


def search(left, right, time, distance, direction):
    while True:
        middle = (left + right) // 2
        if check_value(middle, time, distance) and not check_value(
            middle + direction, time, distance
        ):
            return middle
        if not check_value(middle, time, distance):
            if direction == -1:
                left = middle
            else:
                right = middle
        else:
            if direction == -1:
                right = middle
            else:
                left = middle


def getRange(time: int, distance: int):
    middle = time // 2
    left = 1
    right = time
    left_found = search(left, middle, time, distance, -1)
    right_found = search(middle, right, time, distance, 1)
    return range(left_found, right_found + 1)


def main():
    data = getInput()

    # PART 1
    part_1_answer = 1
    for i in range(len(data["Time"])):
        part_1_answer = part_1_answer * len(
            getRange(int(data["Time"][i]), int(data["Distance"][i]))
        )
    print(f"PART 1: {part_1_answer}")

    # PART 2
    time = ""
    distance = ""
    for i in range(len(data["Time"])):
        time += data["Time"][i]
        distance += data["Distance"][i]
    part_2_answer = len(getRange(int(time), int(distance)))
    print(f"PART 2: {part_2_answer}")


if __name__ == "__main__":
    main()

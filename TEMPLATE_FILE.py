"""https://adventofcode.com/{year}/day/{day}"""

from aoc_util.helper import read


def getInput(test: bool):
    # READ INPUT
    if test:
        data = read("./{year}/inputs/{day}.txt").strip().split("\n")
    else:
        data = read("./{year}/inputs/{day}-test.txt").strip().split("\n")
    # PARSE DATA
    parsed_input = data

    return parsed_input


def main():
    # PART 1
    part_1_answer = None
    print(f"PART 1: {part_1_answer}")

    # PART 2

    part_2_answer = None
    print(f"PART 2: {part_2_answer}")


if __name__ == "__main__":
    main()

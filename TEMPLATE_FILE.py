"""https://adventofcode.com/{year}/day/{day}"""

from pathlib import Path


def getInput(test: bool = False):
    # READ INPUT
    file_path = (
        Path("./{year}/inputs/{day}-test.txt")
        if test
        else Path("./{year}/inputs/{day}.txt")
    )
    data = file_path.read_text().strip().split("\n")
    return data


def main():
    # PART 1
    part_1_answer = None
    print(f"PART 1: {part_1_answer}")

    # PART 2

    part_2_answer = None
    print(f"PART 2: {part_2_answer}")


if __name__ == "__main__":
    main()

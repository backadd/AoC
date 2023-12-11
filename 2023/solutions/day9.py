"""https://adventofcode.com/2023/day/9"""

from pathlib import Path


def getInput(test: bool = False):
    # READ INPUT
    file_path = (
        Path("./2023/inputs/9-test.txt") if test else Path("./2023/inputs/9.txt")
    )
    data = file_path.read_text().strip().split("\n")
    numbers = [[int(n) for n in s.split()] for s in data]
    return numbers


def get_diff(numbers: list):
    new_numbers = []
    for i in range(1, len(numbers)):
        new_numbers.append(numbers[i] - numbers[i - 1])

    return new_numbers


def extrapolate(numbers: list):
    all_numbers = [numbers]
    current_numbers = set(numbers)

    while len(current_numbers) != 1 or 0 not in current_numbers:
        numbers = get_diff(numbers)
        current_numbers = set(numbers)
        all_numbers.append(numbers)

    z_1 = 0
    z_2 = 0
    for i in range(len(all_numbers) - 1, -1, -1):
        # ADD NEW NUBMER TO END OF LIST
        current_list = all_numbers[i]
        y_1 = current_list[-1]
        x_1 = y_1 + z_1
        current_list.append(x_1)
        z_1 = x_1

        # ADD NUMBER TO THE FRONT OF THE LIST
        y_2 = current_list[0]
        x_2 = y_2 - z_2
        current_list.insert(0, x_2)
        z_2 = x_2

    return (all_numbers[0][-1], all_numbers[0][0])


def main():
    data = getInput()

    part_1_answer = 0
    part_2_answer = 0

    for numbers in data:
        a, b = extrapolate(numbers)
        part_1_answer += a
        part_2_answer += b
    # PART 1
    print(f"PART 1: {part_1_answer}")

    # PART 2
    print(f"PART 2: {part_2_answer}")


if __name__ == "__main__":
    main()

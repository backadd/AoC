"""https://adventofcode.com/2023/day/8"""

from math import lcm
from pathlib import Path


def getInput(test: bool = False, second_test: bool = False):
    # READ INPUT
    if test:
        if second_test:
            file_path = Path("./2023/inputs/8-test2.txt")
        else:
            file_path = Path("./2023/inputs/8-test.txt")
    else:
        file_path = Path("./2023/inputs/8.txt")
    instructions, _, *data = file_path.read_text().strip().splitlines()
    node_map = {}
    for line in data:
        node_map[line.split("=")[0].strip()] = (
            line.split("=")[1].strip()[1:-1].split(", ")
        )
    return (instructions, node_map)


def steps_to_z(current_node: str, target: str, instructions: str, node_map: dict):
    i = 0
    while True:
        for direction in instructions:
            if current_node.endswith(target):
                return i
            else:
                current_node = (
                    node_map[current_node][0]
                    if direction == "L"
                    else node_map[current_node][1]
                )
                i += 1


def main():
    instructions, node_map = getInput(False, False)

    # PART 1
    part_1_answer = steps_to_z("AAA", "ZZZ", instructions, node_map)
    print(f"PART 1: {part_1_answer}")

    # PART 2
    A_nodes = [node for node in node_map if node.endswith("A")]
    steps = []
    for node in A_nodes:
        steps.append(steps_to_z(node, "Z", instructions, node_map))

    part_2_answer = lcm(*steps)
    print(f"PART 2: {part_2_answer}")


if __name__ == "__main__":
    main()

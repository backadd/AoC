"""https://adventofcode.com/2023/day/10"""

import math
from pathlib import Path


def getInput(test: bool = False):
    # READ INPUT
    file_path = (
        Path("./2023/inputs/10-test.txt") if test else Path("./2023/inputs/10.txt")
    )
    data = file_path.read_text().strip()
    return data


class Tile:
    def __init__(self, kind: str, coordinates: (int, int)):
        self.kind = kind
        self.connections = []
        self.start = False
        self.distance = math.inf
        self.coordinates = coordinates
        self.inside = True

        if self.kind == "S":
            self.start = True
            self.distance = 0
        self.setConnections(kind)

    def setConnections(self, kind: str):
        if kind == "|":
            self.connections = [
                (self.coordinates[0], self.coordinates[1] - 1),
                (self.coordinates[0], self.coordinates[1] + 1),
            ]
        if kind == "-":
            self.connections = [
                (self.coordinates[0] - 1, self.coordinates[1]),
                (self.coordinates[0] + 1, self.coordinates[1]),
            ]
        if kind == "L":
            self.connections = [
                (self.coordinates[0], self.coordinates[1] - 1),
                (self.coordinates[0] + 1, self.coordinates[1]),
            ]
        if kind == "J":
            self.connections = [
                (self.coordinates[0], self.coordinates[1] - 1),
                (self.coordinates[0] - 1, self.coordinates[1]),
            ]
        if kind == "7":
            self.connections = [
                (self.coordinates[0], self.coordinates[1] + 1),
                (self.coordinates[0] - 1, self.coordinates[1]),
            ]
        if kind == "F":
            self.connections = [
                (self.coordinates[0], self.coordinates[1] + 1),
                (self.coordinates[0] + 1, self.coordinates[1]),
            ]


class Grid:
    def __init__(self, input_data: str):
        self.y = []
        for i, line in enumerate(input_data.split("\n")):
            x = []
            for i2, c in enumerate(line):
                tile = Tile(c, (i2, i))
                if tile.start:
                    self.start = (i2, i)
                x.append(tile)
            self.y.append(x)

        # SET START KIND
        connecting_tiles = []

        left = (self.start[0] - 1, self.start[1])
        right = (self.start[0] + 1, self.start[1])
        over = (self.start[0], self.start[1] - 1)
        under = (self.start[0], self.start[1] + 1)

        if self.getTile(*left) and self.start in self.getTile(*left).connections:
            connecting_tiles.append(left)

        if self.getTile(*right) and self.start in self.getTile(*right).connections:
            connecting_tiles.append(right)

        if self.getTile(*over) and self.start in self.getTile(*over).connections:
            connecting_tiles.append(over)

        if self.getTile(*under) and self.start in self.getTile(*under).connections:
            connecting_tiles.append(under)

        self.most_left_tile = self.start

        for tile in connecting_tiles:
            previous = self.start
            current = self.getTile(*tile)
            self.start_connections = None
            while len(current.connections) > 0:
                for conn in current.connections:
                    if conn != previous:
                        previous = current.coordinates
                        current = self.getTile(*conn)
                        break
                if current.coordinates == self.start:
                    self.start_connections = self.getTile(*tile).coordinates, previous
                    break
            if self.start_connections:
                break

        for tile in self.start_connections:
            previous = self.start
            current = self.getTile(*tile)

            i = 1
            while current.coordinates != self.start:
                if current.coordinates[0] < self.most_left_tile[0]:
                    self.most_left_tile = current.coordinates
                if i < current.distance:
                    current.distance = i
                for conn in current.connections:
                    if conn != previous:
                        previous = current.coordinates
                        current = self.getTile(*conn)
                        break
                i += 1

        self.highest_distance = 0
        self.pipe = {self.start}
        for tile in self.start_connections:
            previous = self.start
            current = self.getTile(*tile)
            while current.coordinates != self.start:
                self.pipe.add(current.coordinates)
                if self.highest_distance < current.distance:
                    self.highest_distance = current.distance
                for conn in current.connections:
                    if conn != previous:
                        previous = current.coordinates
                        current = self.getTile(*conn)
                        break
                i += 1

        # CLEAN SCRAP
        for row in self.y:
            for tile in row:
                if tile.coordinates not in self.pipe:
                    tile.kind = "."

        # SET S KIND
        left = False
        right = False
        up = False
        down = False
        start = self.getTile(*self.start)
        for coordinates in self.start_connections:
            x, y = coordinates
            x2, y2 = self.start

            if x == x2 - 1:
                left = True
            if x == x2 + 1:
                right = True
            if y == y2 - 1:
                up = True
            if y == y2 + 1:
                down = True
        if up and down:
            start.kind = "|"
        if up and right:
            start.kind = "L"
        if up and left:
            start.kind = "J"
        if left and down:
            start.kind = "7"
        if right and down:
            start.kind = "F"
        if left and right:
            start.kind = "-"
        start.setConnections(start.kind)

    def getTile(self, x: int, y: int):
        if x >= 0 and y >= 0 and x < len(self.y[0]) and y < len(self.y):
            return self.y[y][x]
        return None

    def getTileOutsideLoop(self):
        start_tile = self.getTile(*self.most_left_tile)
        outside = set()

        if start_tile.kind == "|":
            outside.add(
                self.getTile(start_tile.coordinates[0] - 1, start_tile.coordinates[1])
            )
        if start_tile.kind == "L":
            outside.add(
                self.getTile(start_tile.coordinates[0] - 1, start_tile.coordinates[1])
            )
            outside.add(
                self.getTile(start_tile.coordinates[0], start_tile.coordinates[1] + 1)
            )
        if start_tile.kind == "F":
            outside.add(
                self.getTile(start_tile.coordinates[0] - 1, start_tile.coordinates[1])
            )
            outside.add(
                self.getTile(start_tile.coordinates[0], start_tile.coordinates[1] - 1)
            )

        up = True
        if start_tile.connections[0][1] < start_tile.connections[1][1]:
            current = self.getTile(*start_tile.connections[0])
            previous = start_tile
        else:
            current = self.getTile(*start_tile.connections[1])
            previous = start_tile

        while current != start_tile:
            if up:
                if current.kind == "|":
                    outside.add(
                        self.getTile(current.coordinates[0] - 1, current.coordinates[1])
                    )
                if current.kind == "L":
                    outside.add(
                        self.getTile(current.coordinates[0] - 1, current.coordinates[1])
                    )
                    outside.add(
                        self.getTile(current.coordinates[0], current.coordinates[1] + 1)
                    )
                if current.kind == "F":
                    outside.add(
                        self.getTile(current.coordinates[0] - 1, current.coordinates[1])
                    )
                    outside.add(
                        self.getTile(current.coordinates[0], current.coordinates[1] - 1)
                    )
                if current.kind == "-":
                    outside.add(
                        self.getTile(current.coordinates[0], current.coordinates[1] - 1)
                    )
            else:
                if current.kind == "|":
                    outside.add(
                        self.getTile(current.coordinates[0] + 1, current.coordinates[1])
                    )
                if current.kind == "-":
                    outside.add(
                        self.getTile(current.coordinates[0], current.coordinates[1] + 1)
                    )
                if current.kind == "7":
                    outside.add(
                        self.getTile(current.coordinates[0] + 1, current.coordinates[1])
                    )
                    outside.add(
                        self.getTile(current.coordinates[0], current.coordinates[1] - 1)
                    )
                if current.kind == "J":
                    outside.add(
                        self.getTile(current.coordinates[0] + 1, current.coordinates[1])
                    )
                    outside.add(
                        self.getTile(current.coordinates[0], current.coordinates[1] + 1)
                    )
            if up and current.kind == "7":
                up = False
            elif not up and current.kind == "L":
                up = True

            while outside:
                tile = outside.pop()
                q = set()
                seen = set()
                if tile and tile.coordinates not in self.pipe:
                    q.add((tile.coordinates[0], tile.coordinates[1]))
                    q.add((tile.coordinates[0], tile.coordinates[1] + 1))
                    q.add((tile.coordinates[0] + 1, tile.coordinates[1]))
                    q.add((tile.coordinates[0], tile.coordinates[1] - 1))
                    q.add((tile.coordinates[0] - 1, tile.coordinates[1] - 1))
                    q.add((tile.coordinates[0] + 1, tile.coordinates[1] - 1))
                    q.add((tile.coordinates[0] - 1, tile.coordinates[1] + 1))
                    q.add((tile.coordinates[0] + 1, tile.coordinates[1] + 1))

                while q:
                    i = q.pop()

                    if i not in self.pipe and i not in seen:
                        tile = self.getTile(*i)
                        if tile:
                            tile.inside = False
                            q.add((tile.coordinates[0] - 1, tile.coordinates[1]))
                            q.add((tile.coordinates[0], tile.coordinates[1] + 1))
                            q.add((tile.coordinates[0] + 1, tile.coordinates[1]))
                            q.add((tile.coordinates[0], tile.coordinates[1] - 1))
                    seen.add(i)
            for con in current.connections:
                if con != previous.coordinates:
                    previous = current
                    current = self.getTile(*con)
                    break

        for tile in outside:
            if tile in self.pipe:
                outside.remove(tile)
        q = set()
        seen = set()
        for tile in outside:
            q.add((tile.coordinates[0] - 1, tile.coordinates[1]))
            q.add((tile.coordinates[0], tile.coordinates[1] + 1))
            q.add((tile.coordinates[0] + 1, tile.coordinates[1]))
            q.add((tile.coordinates[0], tile.coordinates[1] - 1))

        while q:
            i = q.pop()
            seen.add(i)
            if i not in self.pipe and i not in seen:
                tile = self.getTile(*i)
                if tile:
                    tile.inside = False
                    q.add((tile.coordinates[0] - 1, tile.coordinates[1]))
                    q.add((tile.coordinates[0], tile.coordinates[1] + 1))
                    q.add((tile.coordinates[0] + 1, tile.coordinates[1]))
                    q.add((tile.coordinates[0], tile.coordinates[1] - 1))

    def print_distances(self):
        output = ""

        for y in self.y:
            for x in y:
                if x.distance < math.inf:
                    output += str(x.distance)
                else:
                    if x.start:
                        output += "S"
                    else:
                        output += "."
            output += "\n"
        print(output)

    def print_grid(self):
        output = ""

        for y in self.y:
            for x in y:
                if x.distance < math.inf:
                    output += x.kind
                else:
                    if x.start:
                        output += "S"
                    elif x.inside:
                        output += "*"
                    else:
                        output += "."
            output += "\n"
        print(output)
        return output

    def print_current_position(self, coordinates):
        output = ""

        for y in self.y:
            for x in y:
                if x.distance < math.inf:
                    if x.coordinates == coordinates:
                        output += "X"
                    else:
                        output += x.kind
                else:
                    if x.start:
                        output += "S"
                    elif x.inside:
                        output += "*"
                    else:
                        output += "."
            output += "\n"
        print(output)
        return output


def main():
    data = getInput()

    my_grid = Grid(data)
    # my_grid.print_distances()

    my_grid.getTileOutsideLoop()
    printed_grid = my_grid.print_grid()
    # PART 1
    part_1_answer = my_grid.highest_distance
    print(f"PART 1: {part_1_answer}")

    # PART 2

    part_2_answer = printed_grid.count("*")
    print(f"PART 2: {part_2_answer}")


if __name__ == "__main__":
    main()

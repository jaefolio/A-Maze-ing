from dataclasses import dataclass

NORTH = 1       # 0001
EAST = 2        # 0010
SOUTH = 4       # 0100
WEST = 8        # 1000
ALL_WALLS = 15  # 01111


@dataclass
class Maze:
    width: int
    height: int
    entry_point: tuple[int, int]
    exit_point: tuple[int, int]
    walls: list[list[int]]
    blocked: set[tuple[int, int]]

    def open_between(
        self,
        cell1: tuple[int, int],
        cell2: tuple[int, int],
    ) -> None:

        x1, y1 = cell1
        x2, y2 = cell2

        if not (
            0 <= x1 < self.width
            and 0 <= y1 < self.height
            and 0 <= x2 < self.width
            and 0 <= y2 < self.height
        ):
            raise ValueError("Cell coordinates out of bounds")

        dx: int = x2 - x1
        dy: int = y2 - y1

        if abs(dx) + abs(dy) != 1:
            raise ValueError("Cells must be adjacent")

        if cell1 in self.blocked or cell2 in self.blocked:
            raise ValueError("Cannot open walls of blocked cells")

        if dx == 1:  # EAST
            self.walls[y1][x1] &= ~EAST
            self.walls[y2][x2] &= ~WEST
        elif dx == -1:  # WEST
            self.walls[y1][x1] &= ~WEST
            self.walls[y2][x2] &= ~EAST
        elif dy == -1:  # NORTH
            self.walls[y1][x1] &= ~NORTH
            self.walls[y2][x2] &= ~SOUTH
        elif dy == 1:  # SOUTH
            self.walls[y1][x1] &= ~SOUTH
            self.walls[y2][x2] &= ~NORTH

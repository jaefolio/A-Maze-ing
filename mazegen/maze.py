"""Represent maze cells as four wall bits and open shared passages."""

from dataclasses import dataclass

NORTH = 1       # 0001
EAST = 2        # 0010
SOUTH = 4       # 0100
WEST = 8        # 1000
ALL_WALLS = 15  # 1111


@dataclass
class Maze:
    """Store maze geometry, walls, endpoints, and blocked pattern cells.

    Attributes:
        width: Number of columns.
        height: Number of rows.
        entry_point: Entry coordinates as an (x, y) tuple.
        exit_point: Exit coordinates as an (x, y) tuple.
        walls: Row-major grid, accessed as walls[y][x]. Set bits represent
            closed walls: north=1, east=2, south=4, and west=8.
        blocked: Coordinates excluded from traversal, normally the 42 pattern.

    Construction stores the supplied data without validating it.
    """

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
        """Open the shared wall between two adjacent, walkable cells.

        Both cells' wall values are modified in place. Opening an already
        open passage leaves it open.

        Args:
            cell1: First cell's (x, y) coordinates.
            cell2: Second cell's (x, y) coordinates.

        Raises:
            ValueError: A cell is outside the maze, the cells are not
                orthogonally adjacent, or either cell is blocked.
        """
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

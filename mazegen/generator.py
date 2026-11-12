import random
from maze import Maze


Cell = tuple[int, int]

PATTERN_42 = (
    "#...###",
    "#.....#",
    "###.###",
    "..#.#..",
    "..#.###",
)


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        seed: int | None
    ) -> None:

        if width <= 0 or height <= 0:
            raise ValueError("Maze dimensions must be positive")
        self.width = width
        self.height = height
        self.rng = random.Random(seed)

    def _build_initial_tree(
        self,
    ) -> tuple[dict[Cell, Cell | None], Cell]:

        parent: dict[Cell, Cell | None] = {}
        root: Cell = (self.width - 1, self.height - 1)

        for y in range(self.height):
            for x in range(self.width):

                cell = (x, y)

                if cell == root:
                    parent[cell] = None

                elif x < self.width - 1:
                    parent[cell] = (x + 1, y)

                else:
                    parent[cell] = (x, y + 1)

        return parent, root

    def _shift_origin(
        self,
        parent: dict[Cell, Cell | None],
        root: Cell,
    ) -> Cell:

        x, y = root
        directions = [
            (0, -1),
            (1, 0),
            (0, 1),
            (-1, 0),
        ]
        neighbours: list[Cell] = []

        for dx, dy in directions:
            nx = dx + x
            ny = dy + y

            if (0 <= nx < self.width and 0 <= ny < self.height
                    and (nx, ny) in parent):
                neighbours.append((nx, ny))

        if not neighbours:
            return root

        new_root = self.rng.choice(neighbours)
        parent[root] = new_root
        parent[new_root] = None

        return new_root

    def _carve_tree(
        self,
        maze: Maze,
        parent: dict[Cell, Cell | None],
    ) -> None:

        for cell, parent_cell in parent.items():
            if parent_cell is not None:
                maze.open_between(cell, parent_cell)

    def generate(self) -> Maze:
        parent, root = self._build_initial_tree()

        iterations: int = self.width * self.height * 10

        for _ in range(iterations):
            root = self._shift_origin(parent, root)

        maze = Maze(
            width=self.width,
            height=self.height,
            walls=[[15] * self.width for _ in range(self.height)],
            blocked=set(),
            entry_point=(0, 0),
            exit_point=(2, 2),
        )

        self._carve_tree(maze, parent)
        return maze

    def _create_42_pattern(self) -> set[Cell]:
        blocked = set()

        if self.width < 9 or self.height < 7:
            print("Warning: Maze too small for the 42 pattern")
            return blocked

        pattern_height = len(PATTERN_42)
        pattern_width = len(PATTERN_42[0])

        start_x = (self.width - pattern_width) // 2
        start_y = (self.height - pattern_height) // 2

        for dy, row in enumerate(PATTERN_42):
            for dx, char in enumerate(row):
                if char == "#":
                    x = start_x + dx
                    y = start_y + dy
                    blocked.add((x, y))

        return blocked

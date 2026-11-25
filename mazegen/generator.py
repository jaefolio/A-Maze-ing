import random
from .maze import Maze, EAST, SOUTH
from . import validator
from collections.abc import Callable

Cell = tuple[int, int]

PATTERN_42 = (
    "#...###",
    "#.....#",
    "###.###",
    "..#.#..",
    "..#.###",
)

directions = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
]


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
        blocked: set[Cell],
    ) -> tuple[dict[Cell, Cell | None], Cell]:

        root: Cell = (self.width - 1, self.height - 1)

        parent: dict[Cell, Cell | None] = {root: None}
        stack: list[Cell] = [root]

        while stack:
            x, y = stack.pop()

            for dx, dy in directions:
                nx = x + dx
                ny = y + dy

                if (
                    0 <= nx < self.width
                    and 0 <= ny < self.height
                    and (nx, ny) not in blocked
                    and (nx, ny) not in parent
                ):
                    parent[(nx, ny)] = (x, y)
                    stack.append((nx, ny))

        walkable_cells = self.width * self.height - len(blocked)

        if len(parent) != walkable_cells:
            raise ValueError("Walkable cells are disconnected")

        return parent, root

    def _shift_origin(
        self,
        parent: dict[Cell, Cell | None],
        root: Cell,
    ) -> Cell:
        x, y = root

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

    def generate(
            self,
            algorithm: str = "origin_shift",
            perfect: bool = False,
            entry: Cell = (0, 0),
            exit: Cell | None = None,
            on_step: Callable[
                [dict[Cell, Cell | None], Cell], None
            ] | None = None
    ) -> Maze:
        blocked = self._create_42_pattern()

        if exit is None:
            exit = (self.width - 1, self.height - 1)

        for name, (x, y) in (("Entry", entry), ("Exit", exit)):
            if not (0 <= x < self.width and 0 <= y < self.height):
                raise ValueError(f"{name} is outside the maze")

        if entry in blocked:
            raise ValueError("Entry cannot be inside the 42 pattern")

        if exit in blocked:
            raise ValueError("Exit cannot be inside the 42 pattern")

        if entry == exit:
            raise ValueError("Entry and exit can't be the same")

        if algorithm not in ["origin_shift", "dfs"]:
            raise ValueError("Unknown algorithm")

        for _ in range(100):
            if algorithm == "origin_shift":
                parent, root = self._build_initial_tree(blocked)

                if on_step is not None:
                    on_step(parent, root)

                iterations: int = self.width * self.height * 10
                for _ in range(iterations):
                    root = self._shift_origin(parent, root)

                    if on_step is not None:
                        on_step(parent, root)

            else:
                parent, root = self._build_dfs_tree(blocked, on_step)

            maze = Maze(
                width=self.width,
                height=self.height,
                walls=[[15] * self.width for _ in range(self.height)],
                blocked=blocked,
                entry_point=entry,
                exit_point=exit,
            )

            self._carve_tree(maze, parent)

            if perfect:
                return maze

            try:
                self._add_loops(maze)
            except ValueError:
                continue

            if validator.validate_non_perfect(maze):
                return maze

        raise ValueError("Failed to generate a valid non-perfect maze")

    def _create_42_pattern(self) -> set[Cell]:
        blocked: set[Cell] = set()

        if self.width < 9 or self.height < 7:
            print("Warning: Maze too small for the 42 pattern")
            return set()

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

    def _build_dfs_tree(
        self,
        blocked: set[Cell],
        on_step: Callable[
                [dict[Cell, Cell | None], Cell], None
        ] | None = None
    ) -> tuple[dict[Cell, Cell | None], Cell]:

        root: Cell = (self.width - 1), (self.height - 1)

        parent: dict[Cell, Cell | None] = {root: None}
        stack: list[Cell] = [root]

        if on_step is not None:
            on_step(parent, root)

        while stack:
            x, y = stack[-1]

            neighbours: list[Cell] = []

            for dx, dy in directions:
                nx = x + dx
                ny = y + dy

                if (
                    0 <= nx < self.width
                    and 0 <= ny < self.height
                    and (nx, ny) not in blocked
                    and (nx, ny) not in parent
                ):
                    neighbours.append((nx, ny))

            if neighbours:
                new_cell = self.rng.choice(neighbours)

                parent[new_cell] = (x, y)
                stack.append(new_cell)

                if on_step is not None:
                    on_step(parent, new_cell)
            else:
                stack.pop()

                # ANIMATION: there is no current cell after the last pop.
                if on_step is not None and stack:
                    on_step(parent, stack[-1])

        walkable_cells = self.width * self.height - len(blocked)

        if len(parent) != walkable_cells:
            raise ValueError("Walkable cells are disconnected")

        return parent, root

    def _add_loops(self, maze: Maze) -> None:
        candidates: list[tuple[Cell, Cell]] = []

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in maze.blocked:
                    continue

                walls = maze.walls[y][x]

                if (
                    x + 1 < self.width
                    and (walls & EAST)
                    and (x + 1, y) not in maze.blocked
                ):
                    candidates.append(((x, y), (x + 1, y)))

                if (
                    y + 1 < self.height
                    and (walls & SOUTH)
                    and (x, y + 1) not in maze.blocked
                ):
                    candidates.append(((x, y), (x, y + 1)))

        self.rng.shuffle(candidates)

        for cell1, cell2 in candidates:
            neighbour1 = validator.get_accessible_neighbours(maze, cell1)
            neighbour2 = validator.get_accessible_neighbours(maze, cell2)

            # tentative modifcation with rollback if open 3x3 space is found
            if len(neighbour1) == 1 or len(neighbour2) == 1:
                x1, y1 = cell1
                x2, y2 = cell2

                old_walls1 = maze.walls[y1][x1]
                old_walls2 = maze.walls[y2][x2]
                maze.open_between(cell1, cell2)

                if validator.has_open_3x3(maze):
                    maze.walls[y1][x1] = old_walls1
                    maze.walls[y2][x2] = old_walls2
                    continue

            passages = validator.count_passages(maze)

            walkable_cells = (
                maze.width * maze.height - len(maze.blocked)
            )

            cycles = passages - walkable_cells + 1

            if cycles < 2:
                for c1, c2 in candidates:

                    if c2 in validator.get_accessible_neighbours(maze, c1):
                        continue

                    x1, y1 = c1
                    x2, y2 = c2

                    old_walls1 = maze.walls[y1][x1]
                    old_walls2 = maze.walls[y2][x2]
                    maze.open_between(c1, c2)

                    if validator.has_open_3x3(maze):
                        maze.walls[y1][x1] = old_walls1
                        maze.walls[y2][x2] = old_walls2
                        continue

                    cycles += 1

                    if cycles >= 2:
                        break

            if cycles < 2:
                raise ValueError("Unable to create at least 2 cycles")

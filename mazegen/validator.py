from maze import Maze, NORTH, EAST, SOUTH, WEST

Cell = tuple[int, int]


def get_accessible_neighbours(
    maze: Maze,
    cell: Cell,
) -> list[Cell]:

    x, y = cell

    directions = [
     (0, -1, NORTH, SOUTH),
     (1, 0, EAST, WEST),
     (0, 1, SOUTH, NORTH),
     (-1, 0, WEST, EAST),
    ]

    if not (0 <= x < maze.width and 0 <= y < maze.height):
        raise ValueError("Cell coordinates out of bounds")

    if cell in maze.blocked:
        return []

    current_walls = maze.walls[y][x]
    neighbours: list[Cell] = []

    for dx, dy, wall, opposite in directions:
        nx = dx + x
        ny = dy + y

        if (0 <= nx < maze.width and 0 <= ny < maze.height
                and (nx, ny) not in maze.blocked):
            neighbour_walls = maze.walls[ny][nx]

            if (
                not (current_walls & wall)
                and not (neighbour_walls & opposite)
            ):
                neighbours.append((nx, ny))
    return neighbours

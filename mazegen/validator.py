from maze import Maze, NORTH, EAST, SOUTH, WEST, ALL_WALLS

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


def is_connected(maze: Maze) -> bool:
    start = maze.entry_point

    stack: list[Cell] = [start]   # discovered cells needed to be explored
    visited: set[Cell] = {start}  # discovered cells

    while stack:
        current = stack.pop()
        neighbours = get_accessible_neighbours(maze, current)

        for neighbour in neighbours:
            if neighbour not in visited:
                stack.append(neighbour)
                visited.add(neighbour)

    total_cells = maze.width * maze.height
    walkable_cells = total_cells - len(maze.blocked)

    return len(visited) == walkable_cells


def count_passages(maze: Maze) -> int:
    passages: int = 0

    for y in range(maze.height):
        for x in range(maze.width):
            if (x, y) in maze.blocked:
                continue

            current_walls = maze.walls[y][x]

            if x + 1 < maze.width and (x + 1, y) not in maze.blocked:
                if not (current_walls & EAST):
                    passages += 1

            if y + 1 < maze.height and (x, y + 1) not in maze.blocked:
                if not (current_walls & SOUTH):
                    passages += 1

    return passages


def is_perfect(maze: Maze) -> bool:
    if not validate_walls(maze):
        return False

    if not is_connected(maze):
        return False

    total_cells = maze.width * maze.height
    walkable_cells = total_cells - len(maze.blocked)

    return count_passages(maze) == walkable_cells - 1


def validate_walls(maze: Maze) -> bool:
    if maze.width <= 0 or maze.height <= 0:
        return False

    if len(maze.walls) != maze.height:
        return False

    if any(len(row) != maze.width for row in maze.walls):
        return False

    for y in range(maze.height):
        for x in range(maze.width):

            walls = maze.walls[y][x]

            if type(walls) is not int or not 0 <= walls <= 15:
                return False

            if x + 1 < maze.width:
                east_closed = bool(walls & EAST)
                west_closed = bool(maze.walls[y][x + 1] & WEST)
                if east_closed != west_closed:
                    return False

            if y + 1 < maze.height:
                south_closed = bool(walls & SOUTH)
                north_closed = bool(maze.walls[y + 1][x] & NORTH)
                if south_closed != north_closed:
                    return False

            if (
                (y == 0 and not (walls & NORTH))
                or (x == 0 and not (walls & WEST))
                or (y == maze.height - 1 and not (walls & SOUTH))
                or (x == maze.width - 1 and not (walls & EAST))
            ):
                return False

            if (x, y) in maze.blocked:
                if walls != ALL_WALLS:
                    return False

    return True

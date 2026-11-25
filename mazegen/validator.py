"""Inspect wall consistency, connectivity, passages, and maze topology."""

from .maze import Maze, NORTH, EAST, SOUTH, WEST, ALL_WALLS

Cell = tuple[int, int]


def get_accessible_neighbours(
    maze: Maze,
    cell: Cell,
) -> list[Cell]:
    """Return adjacent walkable cells with a passage open on both sides.

    Args:
        maze: Maze with a well-formed wall grid.
        cell: Coordinates to inspect as an (x, y) tuple.

    Returns:
        Accessible cells in north, east, south, west order. Blocked cells
        have no accessible neighbours.

    Raises:
        ValueError: The supplied coordinates are outside the maze.
    """
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
    """Check whether every walkable cell can be reached from the entry.

    Args:
        maze: Maze with valid walls and a walkable, in-bounds entry.

    Returns:
        True when traversal from the entry visits every non-blocked cell.

    Wall structure and endpoint validity are assumed, not checked here.
    The maze is not modified.
    """
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
    """Count passages between non-blocked cells once per shared boundary.

    Args:
        maze: Maze with coherent neighbouring wall values.

    Returns:
        Number of open internal passages. Only east and south boundaries
        are inspected so each passage is counted once.
    """
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
    """Check that the maze's walkable graph is a valid spanning tree.

    Args:
        maze: Maze with valid entry coordinates and blocked-cell metadata.

    Returns:
        True if walls are valid, all walkable cells are connected, and the
        passage count equals the walkable-cell count minus one. Together,
        these conditions mean there are no cycles.
    """
    if not validate_walls(maze):
        return False

    if not is_connected(maze):
        return False

    total_cells = maze.width * maze.height
    walkable_cells = total_cells - len(maze.blocked)

    return count_passages(maze) == walkable_cells - 1


def validate_walls(maze: Maze) -> bool:
    """Check grid shape, wall values, shared boundaries, and blocked cells.

    Args:
        maze: Maze whose wall representation is to be checked.

    Returns:
        True if dimensions are positive, the grid matches those dimensions,
        every wall value is an integer from 0 to 15, shared walls agree,
        exterior walls are closed, and blocked cells are fully closed.

    Connectivity, endpoints, and blocked-coordinate bounds are not checked.
    """
    if maze.width <= 0 or maze.height <= 0:
        return False

    if len(maze.walls) != maze.height:
        return False

    if any(len(row) != maze.width for row in maze.walls):
        return False

    for row in maze.walls:
        for walls in row:
            if type(walls) is not int or not 0 <= walls <= 15:
                return False

    for y in range(maze.height):
        for x in range(maze.width):

            walls = maze.walls[y][x]

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


def has_open_3x3(maze: Maze) -> bool:
    """Detect a 3x3 area with every internal shared wall open.

    Args:
        maze: Maze with a valid, coherent wall grid.

    Returns:
        True if any 3x3 window has all twelve internal passages open.
        Walls around the outside of the window do not affect the result.
    """
    for y in range(maze.height - 2):
        for x in range(maze.width - 2):

            if (x, y) in maze.blocked:
                continue

            fully_open = True

            for dy in range(3):
                for dx in range(3):

                    walls = maze.walls[y + dy][x + dx]

                    east_closed = dx < 2 and bool(walls & EAST)
                    south_closed = dy < 2 and bool(walls & SOUTH)

                    if east_closed or south_closed:
                        fully_open = False

            if fully_open:
                return True
    return False


def count_dead_ends(maze: Maze) -> int:
    """Count walkable cells with exactly one accessible neighbour.

    Args:
        maze: Maze with a valid wall grid and blocked-cell metadata.

    Returns:
        Number of degree-one cells, including dead ends whose other
        adjacent cells are blocked or outside the grid. Isolated cells
        have degree zero and are not counted as dead ends here.
    """
    count = 0

    for y in range(maze.height):
        for x in range(maze.width):
            if (x, y) in maze.blocked:
                continue

            neighbours = get_accessible_neighbours(maze, (x, y))

            if len(neighbours) == 1:
                count += 1

    return count


def validate_key_cells(maze: Maze) -> bool:
    """Check that corners and at least one central cell are not blocked.

    Args:
        maze: Maze with positive dimensions and blocked-cell metadata.

    Returns:
        True if all corners are unblocked and at least one central cell
        is unblocked. Even dimensions produce two central indices along
        that axis, giving two or four candidate central cells.

    This checks blocked-set membership, not passages or connectivity.
    """
    width = maze.width
    height = maze.height

    corners = {
        (0, 0),
        (width - 1, 0),
        (0, height - 1),
        (width - 1, height - 1)
    }

    for corner in corners:
        if corner in maze.blocked:
            return False

    center_x = {width // 2}
    center_y = {height // 2}

    if width % 2 == 0:
        center_x.add(width // 2 - 1)

    if height % 2 == 0:
        center_y.add(height // 2 - 1)

    center_cells = {
        (x, y)
        for x in center_x
        for y in center_y
    }

    if all(cell in maze.blocked for cell in center_cells):
        return False

    return True


def validate_non_perfect(maze: Maze) -> bool:
    """Check the connected, looped layout required for non-perfect mode.

    Args:
        maze: Maze with valid endpoints and blocked-cell metadata.

    Returns:
        True if walls are valid, walkable cells are connected, there is no
        open 3x3 area, key cells are available, there are at least two
        independent cycles, and there are no more than two dead ends.

    For a connected maze, independent cycles equal passages minus
    walkable cells plus one. This function does not modify the maze.
    """
    if not validate_walls(maze):
        return False

    if not is_connected(maze):
        return False

    if has_open_3x3(maze):
        return False

    if not validate_key_cells(maze):
        return False

    total_cells = maze.width * maze.height
    walkable_cells = total_cells - len(maze.blocked)
    cycles = count_passages(maze) - walkable_cells + 1

    if cycles < 2:
        return False

    if count_dead_ends(maze) > 2:
        return False

    return True

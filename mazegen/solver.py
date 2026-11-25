"""Find shortest paths through a maze using breadth-first search."""

from .maze import Maze
from .validator import get_accessible_neighbours


def solve_maze(maze: Maze) -> list[tuple[int, int]]:
    """Find a shortest route from the maze's entry to its exit.

    Args:
        maze: Maze with a well-formed wall grid and valid endpoints.

    Returns:
        Coordinates in traversal order, including both endpoints, or an
        empty list if the exit cannot be reached. Equally short routes are
        resolved using north, east, south, west neighbour order.

    The maze is not modified. Passages must be open on both sides, and
    blocked cells are excluded by get_accessible_neighbours().
    """
    queue: list[tuple[int, int]] = [maze.entry_point]
    visited: set[tuple[int, int]] = {maze.entry_point}
    path: dict[tuple[int, int],
               tuple[int, int] | None] = {maze.entry_point: None}
    read_index: int = 0

    while read_index < len(queue):
        current_x, current_y = queue[read_index]
        read_index += 1

        if (current_x, current_y) == maze.exit_point:
            break
        current = (current_x, current_y)

        for neighbor in get_accessible_neighbours(maze, current):
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
                path[neighbor] = current

    if maze.exit_point not in path:
        return []

    final_path: list[tuple[int, int]] = []
    step: tuple[int, int] | None = maze.exit_point
    while step is not None:
        final_path.append(step)
        step = path[step]
    final_path.reverse()
    return final_path

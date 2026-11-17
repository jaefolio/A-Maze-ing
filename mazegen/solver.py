from .maze import Maze
from .validator import get_accessible_neighbours


def solve_maze(maze: Maze) -> list[tuple[int, int]]:
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

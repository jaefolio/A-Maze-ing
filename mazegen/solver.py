from .maze import Maze, NORTH, EAST, SOUTH, WEST


def solve_maze(maze: Maze) -> list[tuple[int, int]]:
    compass: list[tuple] = [
        (NORTH, 0, -1),
        (SOUTH, 0, 1),
        (WEST, -1, 0),
        (EAST, 1, 0)
    ]
    queue: list[tuple[int, int]] = [maze.entry_point]
    visited: set[tuple[int, int]] = {maze.entry_point}
    path: dict[tuple[int, int],
               tuple[int, int] | None] = {maze.entry_point: None}
    current_cell_wall: int
    read_index: int = 0

    while read_index < len(queue):
        current_x, current_y = queue[read_index]
        read_index += 1

        if (current_x, current_y) == maze.exit_point:
            break
        current_cell_wall = maze.walls[current_y][current_x]
        for direction, dx, dy in compass:
            if (current_cell_wall & direction) == 0:
                neighbor = (current_x + dx, current_y + dy)
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    path[neighbor] = (current_x, current_y)

    if maze.exit_point not in path:
        return []

    final_path: list[tuple[int, int]] = []
    step: tuple[int, int] | None = maze.exit_point
    while step is not None:
        final_path.append(step)
        step = path[step]
    final_path.reverse()
    return final_path

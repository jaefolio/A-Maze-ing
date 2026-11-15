from dataclasses import dataclass


NORTH = 1       # 0001
EAST = 2        # 0010
SOUTH = 4       # 0100
WEST = 8        # 1000
ALL_WALLS = 15  # 1111


@dataclass
class Maze:
    width: int
    height: int
    entry_point: tuple[int, int]
    exit_point: tuple[int, int]
    walls: list[list[int]]
    blocked: set[tuple[int, int]]


def solve_maze(maze: Maze):
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
        cell_wall = maze.walls[current_y][current_x]
        


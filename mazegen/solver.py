from collections import deque
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
	queue = deque([maze.entry_point])
    visited = maze.entry_point


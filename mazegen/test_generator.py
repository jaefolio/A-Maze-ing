import validator
from generator import MazeGenerator
from maze import Maze, EAST
maze = Maze(
    width=2,
    height=2,
    walls=[[15, 15], [15, 15]],
    blocked=set(),
    entry_point=(0, 0),
    exit_point=(1, 1),
)

# Open only the east wall of (0, 0)
maze.walls[0][0] &= ~EAST

print(validator.validate_walls(maze))

from generator import MazeGenerator
from validator import is_connected, is_perfect, validate_walls
from maze import Maze, NORTH, EAST, SOUTH, WEST


for algorithm in ("dfs", "origin_shift"):
    generator = MazeGenerator(10, 10, seed=42)
    maze = generator.generate(algorithm=algorithm)

    print(f"\nAlgorithm: {algorithm}")
    print("Blocked cells:", len(maze.blocked))
    print("Connected:", is_connected(maze))
    print("Perfect:", is_perfect(maze))
    print("Valid walls:", validate_walls(maze))
    print()


def print_maze(maze: Maze) -> None:
    for y in range(maze.height):
        top = ""
        middle = ""

        for x in range(maze.width):
            walls = maze.walls[y][x]

            # Draw north wall
            top += "+" + ("---" if walls & NORTH else "   ")

            # Draw west wall
            middle += "|" if walls & WEST else " "

            # Draw cell contents
            if (x, y) in maze.blocked:
                middle += "###"
            elif (x, y) == maze.entry_point:
                middle += " S "
            elif (x, y) == maze.exit_point:
                middle += " E "
            else:
                middle += "   "

        top += "+"
        middle += "|" if maze.walls[y][-1] & EAST else " "

        print(top)
        print(middle)

    # Draw the bottom boundary
    bottom = ""
    for x in range(maze.width):
        walls = maze.walls[-1][x]
        bottom += "+" + ("---" if walls & SOUTH else "   ")

    print(bottom + "+")


for algorithm in ("origin_shift", "dfs"):
    generator = MazeGenerator(
        width=30,
        height=30,
        seed=42,
    )

    maze = generator.generate(algorithm=algorithm)

    print(f"\nAlgorithm: {algorithm}")
    print_maze(maze)

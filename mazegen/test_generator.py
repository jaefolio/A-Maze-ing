
from generator import MazeGenerator

generator = MazeGenerator(
    width=3,
    height=3,
    seed=42,
)

maze = generator.generate()

for row in maze.walls:
    print("".join(f"{cell:X}" for cell in row))

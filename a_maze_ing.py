from config_parser import parse_config
from mazegen.generator import MazeGenerator
from mazegen.solver import solve_maze
from maze_ui import generate_maze, parse_maze
from pydantic import ValidationError
from pathlib import Path
import os
import sys  # for sys.exit
import typing

os.environ.setdefault("XCURSOR_SIZE", '24')


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    data: dict[str, typing.Any]
    try:
        data = parse_config(sys.argv[1])

        output = Path(data["OUTPUT_FILE"])
        if output.exists() and output.samefile(sys.argv[1]):
            raise ValueError("Output file cannot be the input configs")

        maze = MazeGenerator(
            data["WIDTH"], data["HEIGHT"], data["SEED"]
        ).generate(
            algorithm=data["ALGORITHM"],
            perfect=data["PERFECT"],
            entry=data["ENTRY"],
            exit=data["EXIT"],
        )
        path = solve_maze(maze)
        if not path:
            raise ValueError("No path from entry to exit")

        directions = {
            (0, -1): "N", (1, 0): "E",
            (0, 1): "S", (-1, 0): "W",
        }
        path_string = "".join(
            directions[(x2 - x1, y2 - y1)]
            for (x1, y1), (x2, y2) in zip(path, path[1:])
        )
        with open(data["OUTPUT_FILE"], "w", encoding="utf-8") as file:
            for row in maze.walls:
                file.write("".join(f"{walls:X}" for walls in row) + "\n")
            file.write("\n")
            file.write(f"{maze.entry_point[0]},{maze.entry_point[1]}\n")
            file.write(f"{maze.exit_point[0]},{maze.exit_point[1]}\n")
            file.write(path_string + "\n")
        print(f"Maze saved to {data['OUTPUT_FILE']}")
    except ValidationError as e:
        for error in e.errors():
            print(f"Error: {error['msg']}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Invalid file name: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unknown error occured: {e}")
        sys.exit(1)

    try:
        generate_maze(*parse_maze(data["OUTPUT_FILE"]))
    except Exception as e:
        print(f"Display error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

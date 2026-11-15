from config_parser import parse_config
from mazegen.solver import solve_maze
from pydantic import ValidationError
import sys  # for sys.exit
import typing


def main() -> None:
    data: dict[str, typing.Any]
    try:
        data = parse_config("config.txt")
    except ValidationError as e:
        for error in e.errors():
            print(f"Error: {error["msg"]}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Wrong file name? {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unknown error occured: {e}")
        sys.exit(1)

    #  Generate Maze and pass to validation
    #  here ------------------------------------------

    # Solver
    # solve_maze(maze)

    
    # EXPORT
    # Write the hexadecimal grid, the start/end points, and the path_string to the output file
    # export_to_file(maze, path_string, config.OUTPUT_FILE)

    

    


if __name__ == "__main__":
    main()

from config_parser import parse_config
from pydantic import ValidationError
import typing


def main() -> None:
    data: dict[str, typing.Any]
    try:
        data = parse_config("config.txt")
    except ValidationError as e:
        for error in e.errors():
            print(f"Error: {error["msg"]}")
    except FileNotFoundError as e:
        print(f"Wrong file name? {e}")
    except Exception as e:
        print(f"Unknown error occured: {e}")
    
    #  Generate Maze here
    #  here ------------------------------------------

    

    


if __name__ == "__main__":
    main()

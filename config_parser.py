from pydantic import BaseModel, field_validator
import typing


class MazeValidation(BaseModel):
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool

    @field_validator('ENTRY', 'EXIT', mode='before')
    @classmethod
    def parse_coordinates(cls,
                          value: typing.Any
                          ) -> tuple[int, int] | typing.Any:
        if isinstance(value, str) and ',' in value:
            x, y = value.split(',')
            return (int(x.strip()), int(y.strip()))
        return value


def parse_config(filename: str) -> dict[str, str]:
    items: dict[str, typing.Any] = {}
    item_list: list[str]

    with open(filename, 'r') as file:
        for line in file:
            if line.lstrip().startswith('#') or not line.lstrip():
                continue
            item_list = line.split('=')
            item_list = [item.strip() for item in item_list]
            items.update(([(item_list[0], item_list[1])]))
    MazeValidation(**items)
    return items

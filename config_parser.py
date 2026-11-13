from pydantic import (
	BaseModel,
    field_validator,
    model_validator
)
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

    @model_validator(mode='after')
    def validate_maze(self) -> 'MazeValidation':
        if self.WIDTH < 5 or self.HEIGHT < 5:
            raise ValueError(
                "Maze dimensions must be at least 5x5 "
                "to allow for walls and patterns"
            )
        if not (0 <= self.ENTRY[0] < self.WIDTH and
                0 <= self.ENTRY[1] < self.HEIGHT):
            raise ValueError(
                f"ENTRY coordinates {self.ENTRY} are out of bounds"
            )
        if not (0 <= self.EXIT[0] < self.WIDTH and
                0 <= self.EXIT[1] < self.HEIGHT):
            raise ValueError(
                f"Exit coordinates {self.EXIT} are out of bounds"
            )
        if self.ENTRY == self.EXIT:
            raise ValueError(
                "Entry and Exit have the same coordinates"
            )
        return self


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

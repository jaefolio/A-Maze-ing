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
    SEED: int | None = None
    # ANIMATION: select which generator's steps the MLX viewer will replay.
    ALGORITHM: typing.Literal["origin_shift", "dfs"] = "origin_shift"

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
        if self.WIDTH <= 0 or self.HEIGHT <= 0:
            raise ValueError(
                "Maze dimensions must be positive"
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


def parse_config(filename: str) -> dict[str, typing.Any]:
    items: dict[str, typing.Any] = {}

    with open(filename, 'r') as file:
        for number, line in enumerate(file, start=1):
            if line.lstrip().startswith('#') or not line.lstrip():
                continue
            key, separator, value = line.partition('=')
            if not separator or not key.strip():
                raise ValueError(f"Line {number}: expected KEY=VALUE")
            items[key.strip()] = value.strip()
    return MazeValidation(**items).model_dump()

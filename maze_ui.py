from mlx import Mlx
from dataclasses import dataclass
from typing import Any
from mazegen.generator import MazeGenerator
from mazegen.solver import solve_maze
import random


NORTH = 1 << 0  # 1 (0001)
EAST = 1 << 1   # 2 (0010)
SOUTH = 1 << 2  # 4 (0100)
WEST = 1 << 3   # 8 (1000)

WIDTH = 2400
HEIGHT = 1500
PADDING = 60

BG_COLOR = 0xFF1E1E2E
COLOR_WALL = 0xFFFFFFFF
COLOR_PATH = 0xFF3B82F6
COLOR_START = 0xFF22C55E
COLOR_EXIT = 0xFFEF4444

# keyboard numbers (1 - 5)
KEY_1 = 49  # regenerate maze
KEY_2 = 50  # show/hide shortest path
KEY_3 = 51  # change wall colors
KEY_4 = 52  # exit key


@dataclass
class MazeState:
    m: Mlx
    mlx_ptr: int
    mlx_window: int
    img_ptr: int
    buf: memoryview
    bpp: int
    size_line: int
    grid: list[list[int]]
    start: tuple[int, int]
    exit: tuple[int, int]
    path_str: str
    data: dict[str, Any]
    show_path: bool = True
    wall_color: int = COLOR_WALL


def parse_maze(
        filepath: str
        ) -> tuple[list[list[int]], tuple[int, int], tuple[int, int], str]:
    with open(filepath, 'r', encoding="utf-8") as file:
        lines = [line.strip() for line in file]

    grid: list[list[int]] = []
    idx = 0
    # converts the maze back to integer format
    while idx < len(lines) and lines[idx] != "":
        grid.append([int(ch, 16) for ch in lines[idx]])
        idx += 1

    while idx < len(lines) and lines[idx] == "":
        idx += 1

    sx, sy = map(int, lines[idx].split(','))
    ex, ey = map(int, lines[idx + 1].split(','))
    path_str = lines[idx + 2] if idx + 2 < len(lines) else ""
    return grid, (sx, sy), (ex, ey), path_str


def rebuild_maze(
        data: dict[str, Any], seed: int | None
        ) -> tuple[list[list[int]], tuple[int, int], tuple[int, int], str]:
    maze = MazeGenerator(
        data["WIDTH"], data["HEIGHT"], seed
    ).generate(
        algorithm=data["ALGORITHM"],
        perfect=data["PERFECT"],
        entry=data["ENTRY"],
        exit=data["EXIT"]
    )

    path = solve_maze(maze)
    if not path:
        raise ValueError("No entry from entry to exit")

    directions = {
        (0, -1): "N", (1, 0): "E",
        (0, 1): "S", (-1, 0): "W",
    }
    path_str = "".join(
        directions[(x2 - x1, y2 - y1)]
        for (x1, y1), (x2, y2) in zip(path, path[1:])
    )

    return maze.walls, maze.entry_point, maze.exit_point, path_str


def draw_block(
        buf: memoryview,
        size_line: int,
        bpp: int,
        x: int,
        y: int,
        w: int,
        h: int,
        color: int) -> None:
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(WIDTH, x + w)
    y1 = min(HEIGHT, y + h)
    if x0 >= x1 or y0 >= y1:
        return

    bytes_per_pixel = bpp // 8
    row_bytes = color.to_bytes(4, byteorder='little') * (x1 - x0)
    row_len = len(row_bytes)
    for py in range(y0, y1):
        offset = (py * size_line) + (x0 * bytes_per_pixel)
        buf[offset: offset + row_len] = row_bytes


def draw_walls(
        maze: MazeState,
        tile: int,
        wall_t: int,
        offset_x: int,
        offset_y: int
        ) -> None:
    rows = len(maze.grid)
    cols = len(maze.grid[0])
    color = maze.wall_color
    print(color)
    for y in range(rows):
        for x in range(cols):
            cell = maze.grid[y][x]
            px = offset_x + x * tile
            py = offset_y + y * tile

            if cell & NORTH:
                draw_block(
                    maze.buf, maze.size_line, maze.bpp,
                    px, py,
                    tile + wall_t, wall_t,
                    color
                )
            if y == rows - 1 and cell & SOUTH:
                draw_block(
                    maze.buf, maze.size_line, maze.bpp,
                    px, py + tile,
                    tile + wall_t, wall_t,
                    color
                )
            if cell & WEST:
                draw_block(
                    maze.buf, maze.size_line, maze.bpp,
                    px, py,
                    wall_t, tile + wall_t,
                    color
                )
            if x == cols - 1 and cell & EAST:
                draw_block(
                    maze.buf, maze.size_line, maze.bpp,
                    px + tile, py,
                    wall_t, tile + wall_t,
                    color
                )


def draw_maze(maze: MazeState) -> None:
    rows: int = len(maze.grid)
    cols: int = len(maze.grid[0])
    # 48 pixels per tile
    tile: int = max(4, min((WIDTH - PADDING * 2) // cols,
                           (HEIGHT - PADDING * 2) // rows))
    wall_t: int = max(1, tile // 10)
    offset_x: int = (WIDTH - (cols * tile + wall_t)) // 2
    offset_y: int = (HEIGHT - (rows * tile + wall_t)) // 2
    line_t = max(2, tile // 5)
    margin = (tile + wall_t - line_t) // 2

    # window background color
    draw_block(maze.buf, maze.size_line, maze.bpp,
               0, 0, WIDTH, HEIGHT, BG_COLOR)

    current_x, current_y = maze.start
    moves = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
    corridor = tile - wall_t
    inner = max(2, corridor * 3 // 5)
    pad = wall_t + (corridor - inner) // 2
    # pad = max(1, wall_t + tile // 6)
    # inner = max(1, tile - pad * 2)

    # path coloring
    for step in maze.path_str:
        direction_x, direction_y = moves[step]
        next_x = current_x + direction_x
        next_y = current_y + direction_y
        x1 = offset_x + current_x * tile + margin
        y1 = offset_y + current_y * tile + margin
        x2 = offset_x + next_x * tile + margin
        y2 = offset_y + next_y * tile + margin

        x = min(x1, x2)
        y = min(y1, y2)
        w = abs(x2 - x1) + line_t
        h = abs(y2 - y1) + line_t

        draw_block(maze.buf, maze.size_line, maze.bpp,
                   x, y, w, h, COLOR_PATH)
        current_x = next_x
        current_y = next_y

    # starting coords
    draw_block(
        maze.buf, maze.size_line, maze.bpp,
        offset_x + maze.start[0] * tile + pad,
        offset_y + maze.start[1] * tile + pad,
        inner, inner, COLOR_START,
    )
    
    # ending coords
    draw_block(
        maze.buf, maze.size_line, maze.bpp,
        offset_x + maze.exit[0] * tile + pad,
        offset_y + maze.exit[1] * tile + pad,
        inner, inner,
        COLOR_EXIT
    )
    draw_walls(maze, tile, wall_t, offset_x, offset_y)


def on_close(param: tuple[Mlx, int]) -> int:
    m, mlx_ptr = param
    m.mlx_loop_exit(mlx_ptr)
    return 0


def on_key(keycode: int, maze: MazeState) -> int:
    """
    Based on key pressed from numbers within 1 - 5,
    handles its respective events from regenerating the maze
    to changing the wall color of the maze
    
    """
    if keycode == KEY_1:
        new_seed: int = random.randint(0, 2**32 - 1)
        grid, start, exit, path_str = rebuild_maze(maze.data, new_seed)
        maze.grid = grid
        maze.start = start
        maze.exit = exit
        maze.path_str = path_str
        draw_maze(maze)
        maze.m.mlx_put_image_to_window(
            maze.mlx_ptr, maze.mlx_window, maze.img_ptr, 0, 0
        )
        maze.m.mlx_do_sync(maze.mlx_ptr)

    if keycode == KEY_2:
        pass
    if keycode == KEY_3:
        r = random.randint(100, 255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)
        maze.wall_color = (0xFF << 24) | (r << 16) | (g << 8) | b
        draw_maze(maze)
        maze.m.mlx_put_image_to_window(
            maze.mlx_ptr, maze.mlx_window, maze.img_ptr, 0, 0
            )
        maze.m.mlx_do_sync(maze.mlx_ptr)
    if keycode == KEY_4:
        maze.m.mlx_loop_exit(maze.mlx_ptr)
    return 0


def generate_maze(grid: list[list[int]],
                  start: tuple[int, int],
                  exit: tuple[int, int],
                  path_str: str,
                  data: dict[str, Any]
                  ) -> None:
    m = Mlx()
    mlx_ptr = m.mlx_init()
    mlx_window = m.mlx_new_window(mlx_ptr, WIDTH, HEIGHT, "A_maze_ing")

    img_ptr = m.mlx_new_image(mlx_ptr, WIDTH, HEIGHT)
    buf, bpp, size_line, _endian = m.mlx_get_data_addr(img_ptr)

    maze = MazeState(
            m=m,
            mlx_ptr=mlx_ptr,
            mlx_window=mlx_window,
            img_ptr=img_ptr,
            buf=buf,
            bpp=bpp,
            size_line=size_line,
            grid=grid,
            start=start,
            exit=exit,
            path_str=path_str,
            data=data
    )

    draw_maze(maze)

    m.mlx_put_image_to_window(mlx_ptr, mlx_window, img_ptr, 0, 0)
    m.mlx_key_hook(mlx_window, on_key, maze)
    m.mlx_hook(mlx_window, 33, 0, on_close, (m, mlx_ptr))

    m.mlx_loop(mlx_ptr)

    m.mlx_destroy_image(mlx_ptr, img_ptr)
    m.mlx_destroy_window(mlx_ptr, mlx_window)
    m.mlx_release(mlx_ptr)

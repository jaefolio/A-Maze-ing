from mlx import Mlx  # type: ignore


NORTH = 1 << 0  # 1 (0001)
EAST = 1 << 1   # 2 (0010)
SOUTH = 1 << 2  # 4 (0100)
WEST = 1 << 3   # 8 (1000)

WIDTH = 1920
HEIGHT = 1080
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
KEY_4 = 52  # change "42" pattern colors
KEY_5 = 53  # exit key


def parse_maze(
        filepath: str
        ) -> tuple[list[list[int]], tuple[int, int], tuple[int, int], str]:
    with open(filepath, 'r', encoding="utf-8") as file:
        lines = [line.strip() for line in file]

    grid: list[list[int]] = []
    idx = 0
    while idx < len(lines) and lines[idx] != "":
        grid.append([int(ch, 16) for ch in lines[idx]])
        idx += 1

    while idx < len(lines) and lines[idx] == "":
        idx += 1

    sx, sy = map(int, lines[idx].split(','))
    ex, ey = map(int, lines[idx + 1].split(','))
    path_str = lines[idx + 2] if idx + 2 < len(lines) else ""
    return grid, (sx, sy), (ex, ey), path_str


def draw_rectangle(
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


def draw_maze(buf: memoryview,
              size_line: int,
              bpp: int,
              grid: list[list[int]],
              start: tuple[int, int],
              exit: tuple[int, int],
              path_str: str) -> None:
    rows: int = len(grid)
    cols: int = len(grid[0])
    tile: int = max(4, min((WIDTH - PADDING * 2) // cols,
                           (HEIGHT - PADDING * 2) // rows))
    wall_t: int = max(1, tile // 10)
    offset_x: int = (WIDTH - cols * tile) // 2
    offset_y: int = (HEIGHT - rows * tile) // 2

    # window background color
    draw_rectangle(buf, size_line, bpp, 0, 0, WIDTH, HEIGHT, BG_COLOR)

    cx, cy = start
    moves = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
    pad = max(1, wall_t + tile // 6)
    inner = max(1, tile - pad * 2)

    # starting coords
    draw_rectangle(
        buf, size_line, bpp,
        offset_x + start[0] * tile + pad,
        offset_y + start[1] * tile + pad,
        inner, inner, COLOR_START,
    )

    # path coloring
    for step in path_str:
        dx, dy = moves[step]
        cx += dx
        cy += dy
        draw_rectangle(
            buf, size_line, bpp,
            offset_x + cx * tile + pad,
            offset_y + cy * tile + pad,
            inner, inner, COLOR_PATH,
        )

    # ending coords
    draw_rectangle(
        buf, size_line, bpp,
        offset_x + exit[0] * tile + pad,
        offset_y + exit[1] * tile + pad,
        inner, inner, COLOR_EXIT,
    )

    for y in range(rows):
        for x in range(cols):
            cell = grid[y][x]
            px = offset_x + x * tile
            py = offset_y + y * tile

            if cell & NORTH:
                draw_rectangle(
                    buf, size_line, bpp,
                    px, py, tile, wall_t, COLOR_WALL
                )
            if y == rows - 1 and cell & SOUTH:
                draw_rectangle(
                    buf, size_line, bpp,
                    px, py + tile - wall_t, tile, wall_t, COLOR_WALL
                )
            if cell & WEST:
                draw_rectangle(
                    buf, size_line, bpp,
                    px, py, wall_t, tile, COLOR_WALL
                )
            if x == cols - 1 and cell & EAST:
                draw_rectangle(
                    buf, size_line, bpp,
                    px + tile - wall_t, py, wall_t, tile, COLOR_WALL
                )


def on_close(param: tuple[Mlx, int]) -> int:
    m, mlx_ptr = param
    m.mlx_loop_exit(mlx_ptr)
    return 0


def on_key(keycode: int, param: tuple[Mlx, int]) -> int:
    m, mlx_ptr = param
    if keycode == KEY_5:
        m.mlx_loop_exit(mlx_ptr)
    return 0


def generate_maze(grid: list[list[int]],
                  start: tuple[int, int],
                  exit: tuple[int, int],
                  path_str: str) -> None:
    m = Mlx()
    mlx_ptr = m.mlx_init()
    mlx_window = m.mlx_new_window(mlx_ptr, WIDTH, HEIGHT, "A_maze_ing")

    img_ptr = m.mlx_new_image(mlx_ptr, WIDTH, HEIGHT)
    buf, bpp, size_line, _endian = m.mlx_get_data_addr(img_ptr)

    draw_maze(buf, size_line, bpp, grid, start, exit, path_str)

    m.mlx_put_image_to_window(mlx_ptr, mlx_window, img_ptr, 0, 0)
    m.mlx_key_hook(mlx_window, on_key, (m, mlx_ptr))
    m.mlx_hook(mlx_window, 17, 0, on_close, (m, mlx_ptr))

    m.mlx_loop(mlx_ptr)

    m.mlx_destroy_image(mlx_ptr, img_ptr)
    m.mlx_destroy_window(mlx_ptr, mlx_window)
    m.mlx_release(mlx_ptr)
